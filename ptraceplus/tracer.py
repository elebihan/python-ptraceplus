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

"""
Process tracing helper
"""

import os
import signal
import ptraceminus as ptrace
from collections import OrderedDict
from gettext import gettext as _
from .process import TracedProcess, create_process_event, SignalEvent
from .utils import spawn_child
from .common import debug

class TracerError(Exception):
    """Error raised when a tracing operation failed"""

class Tracer(object):
    """Trace a process"""
    def __init__(self):
        self._procs = OrderedDict()
        self._fork_enabled = False
        self._exec_enabled = False
        self._sysgood_enabled = False
        self._options = 0

    def __getitem__(self, key):
        return self._procs[key]

    def __iter__(self):
        return self._procs.itervalues()

    def __contains__(self, key):
        return key in self._procs

    @property
    def has_processes(self):
        return (len(self._procs) != 0)

    def _set_fork_enabled(self, value):
        mask = ptrace.O_TRACEFORK | ptrace.O_TRACEVFORK
        if value:
            self._options |= mask
        else:
            self._options &= ~mask
        self._fork_enabled = value

    def _get_fork_enabled(self):
        return self._fork_enabled

    fork_enabled = property(_get_fork_enabled, _set_fork_enabled,
                            None,
                            "Enable fork tracing")

    def _set_exec_enabled(self, value):
        mask = ptrace.O_TRACEEXEC | ptrace.O_TRACEEXIT
        if value:
            self._options |= mask
        else:
            self._options &= ~mask
        self._exec_enabled = value

    def _get_exec_enabled(self):
        return self._exec_enabled

    exec_enabled = property(_get_exec_enabled, _set_exec_enabled,
                            None,
                            "Enable exec tracing")

    def _set_sysgood_enabled(self, value):
        mask = ptrace.O_TRACESYSGOOD
        if value:
            self._options |= mask
        else:
            self._options &= ~mask
        self._sysgood_enabled = value

    def _get_sysgood_enabled(self):
        return self._sysgood_enabled

    sysgood_enabled = property(_get_sysgood_enabled, _set_sysgood_enabled,
                              None,
                              """Enable sysgood: ask the kernel to set bit
                              #7 of the signal number if the signal comes
                              from kernel space. It is unset if it comes
                              from user space""")

    def spawn_process(self, args, env=None, quiet=True):
        flags = 0
        pid = spawn_child(args, env, quiet)
        pid, status = os.waitpid(pid, flags)
        proc = self.add_process(pid)
        proc.syscall()
        return proc

    def add_process(self, pid, is_attached=True, parent=None):
        if pid in self._procs:
            raise TracerError(_('Process {} already registered').format(pid))
        debug(_("Adding process {}").format(pid))
        proc = self.keep_process(pid, parent)
        if not is_attached:
            proc.attach()
        proc.options = self._options
        return proc

    def keep_process(self, pid, parent=None):
        if pid in self._procs:
            debug(_("Remembering process {}").format(pid))
            return self._procs[pid]

        if parent:
            details = "({})".format(parent.pid)
        else:
            details = ''
        debug(_("Keeping process {} {}").format(pid, details))
        proc = TracedProcess(pid, parent)
        self._procs[pid] = proc
        return proc

    def remove_process(self, pid):
        debug(_("Removing process {}").format(pid))
        try:
            proc = self._procs.pop(pid)
        except KeyError:
            raise TracerError(_('Process not found'))
        proc.terminate()
        proc.detach()
        debug(_("{} processes still traced").format(len(self._procs)))

    def wait_for_event(self, wanted_pid=None, blocking=True):
        flags = 0
        if not blocking:
            flags |= os.WNOHANG
        if wanted_pid and wanted_pid not in self._procs:
            raise TracerError(_("Unknown PID ({})").format(wanted_pid))
        pid = wanted_pid or -1
        pid, status = os.waitpid(pid, flags)
        return create_process_event(pid, status)

    def wait_for_signal(self, *signals, **kwargs):
        pid = kwargs.get('pid', None)
        while True:
            event = self.wait_for_event(pid)
            if isinstance(event, SignalEvent):
                if event.signum in signals or not signals:
                    return event

    def wait_for_syscall(self, pid=None):
        return self.wait_for_signal(signal.SIGTRAP, pid)

    def quit(self):
        while self._procs:
            pid, proc = self._procs.popitem()
            debug(_("Removing process {}").format(pid))
            proc.terminate()
            proc.detach()

# vim: ts=4 sts=4 sw=4 sta et ai
