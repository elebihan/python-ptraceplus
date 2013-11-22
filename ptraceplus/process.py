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
Traced process management
"""

import os
import signal
import ptraceminus as ptrace
from gettext import gettext as _
from .common import debug
from .syscalls.helpers import create_syscall

class UnknownEventError(Exception):
    """Error raised when process status can not be decoded"""

class ProcessEvent(object):
    """Event occuring during process execution"""
    def __init__(self, pid):
        self._pid = pid

    @property
    def pid(self):
        return self._pid

    def __str__(self):
        return "ProcessEvent<{}>".format(self._pid)

class ExecutionEvent(ProcessEvent):
    """Event indicating the execution of a process"""
    def __init__(self, pid):
        ProcessEvent.__init__(self, pid)

    def __str__(self):
        return _("[{}] starting").format(self._pid)

class ForkEvent(ProcessEvent):
    """Event indicating a process has forked"""
    def __init__(self, pid, cpid):
        ProcessEvent.__init__(self, pid)
        self._cpid = cpid

    @property
    def child_pid(self):
        return self._cpid

    def __str__(self):
        return _("[{}] forked as {}").format(self._pid, self._cpid)

class SignalEvent(ProcessEvent):
    """Process received a signal during execution"""
    def __init__(self, pid, signum):
        ProcessEvent.__init__(self, pid)
        if signum & 0x80:
            self._signum = signum & ~0x80
            self._is_syscall = True
        else:
            self._signum = signum
            self._is_syscall = False

    @property
    def signum(self):
        return self._signum

    @property
    def is_syscall(self):
        return self._is_syscall

    def __str__(self):
        if self._is_syscall:
            extra = '(syscall)'
        else:
            extra = ''
        desc = _("[{}] received signal {} {}")
        return desc.format(self._pid, self._signum, extra)

class ExitingEvent(ProcessEvent):
    """Process is about to exit"""
    def __init__(self, pid, status):
        ProcessEvent.__init__(self, pid)
        self._status = status

    @property
    def status(self):
        return self._status

    def __str__(self):
        desc = _("[{}] is about to exit with status {}")
        return desc.format(self._pid, self._status)

class ExitedEvent(ProcessEvent):
    """Process has exited"""
    def __init__(self, pid, code):
        ProcessEvent.__init__(self, pid)
        self._code = code

    @property
    def code(self):
        return self._code

    def __str__(self):
        desc = _("[{}] has exited with code {}")
        return desc.format(self._pid, self._code)

class KilledEvent(ProcessEvent):
    """Process was terminated by a signal"""
    def __init__(self, pid, signum):
        ProcessEvent.__init__(self, pid)
        self._signum = signum

    @property
    def signum(self):
        return self._signum

    def __str__(self):
        desc = _("[{}] killed by signal {}")
        return desc.format(self._pid, self._signum)

def create_process_event(pid, status):
    """Create a process event from PID and status.

    :param pid: PID of the process.
    :type pid: int

    :param status: status of the process.
    :type status: int.

    :returns: an event.
    :rtype: :class:`ptraceplus.process.ProcessEvent`.
    """
    if os.WIFEXITED(status):
        code = os.WEXITSTATUS(status)
        event = ExitedEvent(pid, code)
    elif os.WIFSIGNALED(status):
        signum = os.WTERMSIG(status)
        event = KilledEvent(pid, signum)
    elif os.WIFSTOPPED(status):
        signum = os.WSTOPSIG(status)
        if (signum & ~0x80) == signal.SIGTRAP:
            pevent = (status >> 16) & 0xffffffff
            if pevent == ptrace.EVENT_EXEC:
                event = ExecutionEvent(pid)
            elif pevent in (ptrace.EVENT_FORK, ptrace.EVENT_VFORK):
                cpid = ptrace.getventmsg(pid)
                event = ForkEvent(pid, cpid)
            elif pevent == ptrace.EVENT_EXIT:
                code = ptrace.getventmsg(pid)
                event = ExitingEvent(pid, code)
            else:
                event = SignalEvent(pid, signum)
        else:
            event = SignalEvent(pid, signum)
    else:
        msg = _("Unknown event for {} ({})")
        raise UnknownEventError(msg.format(pid, status))
    return event

class TracedProcess(object):
    """Process traced by a tracer.

    :param pid: PID of the process.
    :type pid: int.

    :param parent: parent of the process (or None).
    :type parent: :class:`ptraceplus.process.TracedProcess`.
    """
    def __init__(self, pid, parent=None):
        self._pid = pid
        self._parent = parent
        self._is_stopped = False
        self._is_attached = False
        self._options = 0
        self._syscall = None

    def _set_options(self, value):
        self._options = value
        ptrace.setoptions(self._pid, self._options)

    def _get_options(self):
        return self.options

    options = property(_get_options, _set_options, None, "Trace options")

    @property
    def pid(self):
        return self._pid

    @property
    def is_stopped(self):
        return self._is_stopped

    @property
    def system_call(self):
        return self._syscall

    def attach(self):
        if not self._is_attached:
            debug(_("Attaching {}").format(self._pid))
            ptrace.attach(self._pid)
            self._is_attached = True

    def detach(self):
        if self._is_attached:
            debug(_("Detaching {}").format(self._pid))
            ptrace.detach(self._pid)
            self._is_attached = False

    def terminate(self):
        pass

    def kill(self, signum):
        os.kill(self._pid, signum)

    def syscall(self, signum=0):
        if signum == signal.SIGTRAP:
            signum = 0
        ptrace.syscall(self._pid, signum)
        self._is_stopped = False

    def cont(self, signum=0):
        if signum == signal.SIGTRAP:
            signum = 0
        ptrace.cont(self._pid, signum)
        self._is_stopped = False

    def prepare_syscall_enter(self):
        syscall = create_syscall(self._pid)
        self._syscall = syscall
        return syscall

    def prepare_syscall_exit(self):
        syscall = self._syscall
        self._syscall = None
        return syscall

# vim: ts=4 sts=4 sw=4 sta et ai
