# -*- coding: utf-8 -*-
#
# python-ptraceplus - Ptrace bindings + extra stuff
#
# Copyright (c) 2013 Eric Le Bihan <eric.le.bihan.dev@free.fr>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import signal
from ptraceplus.tracer import Tracer
from ptraceplus.process import (SignalEvent, ForkEvent, ExecutionEvent,
                                ExitingEvent, ExitedEvent, KilledEvent)

class TracerPlus(object):
    """Simple process tracer.

    :param arguments: arguments of the program to execute and trace.
    :type arguments: list of str.

    :param env: environment variables for the process.
    :type env: mapping between strings

    :param quiet: if True, the output of the program will not be printed.
    :type quiet: bool
    """
    def __init__(self, arguments, env=None, quiet=True):
        self._args = arguments
        self._env = env
        self._quiet = quiet
        self._n_procs = 0

    @property
    def n_procs(self):
        return self._n_procs

    def run(self):
        """Run the tracer"""

        tracer = Tracer()
        tracer.fork_enabled = True
        tracer.exec_enabled = False
        tracer.sysgood_enabled = True

        proc = tracer.spawn_process(self._args, self._env, self._quiet)
        self._n_procs += 1
        self._on_tracing_started(proc)

        while True:
            if not tracer.has_processes:
                break
            event = tracer.wait_for_event()
            self._on_event(event)
            if isinstance(event, SignalEvent):
                # The tracer can be notified of a child receiving a SIGSTOP
                # before the notification of the fork!
                if event.signum == signal.SIGSTOP:
                    if event.pid not in tracer:
                        proc = tracer.remember_process(event.pid)
                    else:
                        proc = tracer[event.pid]
                    proc.syscall()
                else:
                    proc = tracer[event.pid]
                    if event.is_syscall:
                        if proc.system_call is None:
                            syscall = proc.prepare_syscall_enter()
                            self._on_syscall_enter(syscall)
                        else:
                            syscall = proc.prepare_syscall_exit()
                            self._on_syscall_exit(syscall)
                    proc.syscall(event.signum)
            elif isinstance(event, ForkEvent):
                self._n_procs += 1
                parent = tracer[event.pid]
                tracer.remember_process(event.child_pid, parent)
                parent.syscall()
            elif isinstance(event, ExitingEvent):
                self._on_exiting(event)
                proc = tracer[event.pid]
                proc.cont()
            elif isinstance(event, KilledEvent):
                pass
            elif isinstance(event, ExitedEvent):
                self._on_exit(event)
                tracer.remove_process(event.pid)
            elif isinstance(event, ExecutionEvent):
                proc = tracer[event.pid]
                proc.syscall()

        tracer.quit()

    def _on_tracing_started(self, proc):
        pass

    def _on_event(self, event):
        pass

    def _on_syscall_enter(self, syscall):
        pass

    def _on_syscall_exit(self, syscall):
        pass

    def _on_exiting(self, event):
        pass

    def _on_exit(self, event):
        pass

# vim: ts=4 sts=4 sw=4 sta et ai
