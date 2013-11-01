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
from collections import namedtuple
from ptraceplus.tracer import Tracer
from ptraceplus.process import (SignalEvent, ForkEvent, ExecutionEvent,
                                ExitingEvent, ExitedEvent, KilledEvent)

TracerPlusStats = namedtuple('TracerPlusStats', ('n_procs'))

class TracerPlus(object):
    """Simple process tracer.

    :param arguments: arguments of the process to execute and trace.
    :type arguments: list of str.

    :param env: environment variables for the process.
    :type env: mapping between strings
    """
    def __init__(self, arguments, env=None):
        self._args = arguments
        self._env = env
        self._n_procs = 0
        self.verbose = False

    @property
    def stats(self):
        return TracerPlusStats(self._n_procs)

    def run(self):
        """Run the tracer"""

        tracer = Tracer()
        tracer.fork_enabled = True
        tracer.exec_enabled = True
        tracer.sysgood_enabled = True
        tracer.spawn_process(self._args, self._env)

        self._n_procs += 1

        while True:
            if not tracer.has_processes:
                break
            event = tracer.wait_for_syscall()
            if self.verbose:
                print(event)
            if isinstance(event, SignalEvent):
                # The tracer can be notified of a child receiving a SIGSTOP
                # before the notification of the fork!
                if event.signum == signal.SIGSTOP:
                    if event.pid not in tracer:
                        proc = tracer.remember_process(event.pid)
                    else:
                        proc = tracer[event.pid]
                    proc.cont()
                else:
                    proc = tracer[event.pid]
                    proc.syscall(event.signum)
            elif isinstance(event, ForkEvent):
                self._n_procs += 1
                parent = tracer[event.pid]
                tracer.remember_process(event.child_pid, parent)
                parent.cont()
            elif isinstance(event, ExitingEvent):
                proc = tracer[event.pid]
                proc.cont()
                tracer.remove_process(event.pid)
            elif isinstance(event, KilledEvent):
                pass
            elif isinstance(event, ExitedEvent):
                pass
            elif isinstance(event, ExecutionEvent):
                proc = tracer[event.pid]
                proc.syscall()

        tracer.quit()

# vim: ts=4 sts=4 sw=4 sta et ai
