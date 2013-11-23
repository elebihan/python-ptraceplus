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
Collects information about a system call
"""

import abc
import ptraceminus as ptrace
from gettext import gettext as _

(SYSCALL_STATE_UNKNOWN, SYSCALL_STATE_ENTER, SYSCALL_STATE_EXIT) = range(0, 3)

_SYSCALL_STATES = {
    SYSCALL_STATE_UNKNOWN: _('unknown'),
    SYSCALL_STATE_ENTER: _('enter'),
    SYSCALL_STATE_EXIT: _('exit'),
}

(SYSCALL_PARAM_TYPE_STR, SYSCALL_PARAM_TYPE_ADDR, SYSCALL_PARAM_TYPE_NB) = \
        range(0, 3)

class SyscallParamError(Exception):
    """Error raised when collecting system call parameter fails"""

class SyscallParam(object):
    """Represents a Syscall parameter.

    :param type: type of the parameter.
    :type type: str.

    :param name: name of the parameter.
    :type name: str.

    :param value: value of the parameter.
    :type value: int.
    """

    def __init__(self, t, n, v):
        self.type = t
        self.name = n
        self.value = v
        self.pvalue = None
        if self.name in ('filename', 'pathname', 'oldname', 'newname'):
            self._t = SYSCALL_PARAM_TYPE_STR
        elif '*' in self.type:
            self._t = SYSCALL_PARAM_TYPE_ADDR
        else:
            self._t = SYSCALL_PARAM_TYPE_NB

    def __str__(self):
        if self.pvalue and self.is_string:
            fmt = "\"{}\""
            value = self.pvalue.replace('\n', '\\n')
        else:
            if self.is_address:
                fmt = "{:#x}"
            else:
                fmt = "{}"
            value = self.value
        return fmt.format(value)

    @property
    def is_string(self):
        if self._t == SYSCALL_PARAM_TYPE_STR:
            return True
        else:
            return False

    @property
    def is_address(self):
        if self._t == SYSCALL_PARAM_TYPE_ADDR:
            return True
        else:
            return False

class Syscall(object):
    """Represents a system call.

    :param pid: process identifier
    :type pid: int
    """

    __meta__ = abc.ABCMeta

    def __init__(self, pid):
        self._pid = pid
        self._num = ptrace.getscnr(pid)
        self._state = SYSCALL_STATE_ENTER
        self._params = []
        self._result = None

    @property
    def name(self):
        try:
            return self._get_name()
        except KeyError:
            return 'unknown'

    @property
    def num(self):
        return self._num

    @property
    def pid(self):
        return self._pid

    @property
    def prototype(self):
        try:
            return self._get_proto()
        except KeyError:
            return [('?', '?')]

    @property
    def params(self):
        return self._params

    @property
    def result(self):
        return self._result

    @property
    def state(self):
        return self._state

    @abc.abstractmethod
    def _get_result_from_regs(self, regs):
        return

    @abc.abstractmethod
    def _get_name(self):
        return

    @abc.abstractmethod
    def _get_proto(self):
        return

    @abc.abstractmethod
    def _get_params_from_regs(self, regs):
        return

    def __str__(self):
        state = _SYSCALL_STATES[self.state]
        txt = "Syscall {} ({}) for {} ({})"
        return txt.format(self.num, self.name, self.pid, state)

    def collect_params(self):
        regs = ptrace.getregs(self._pid)
        values = self._get_params_from_regs(regs)
        params = []
        for (t, n), v in zip(self.prototype, values):
            param = self._format_param(t, n, v)
            params.append(param)
        self._params = params
        return self._params

    def collect_result(self):
        self._state = SYSCALL_STATE_EXIT
        regs = ptrace.getregs(self._pid)
        self._result = self._get_result_from_regs(regs)
        return self._result

    def _format_param(self, t, n, v):
        param = SyscallParam(t, n, v)
        if param.is_string:
            try:
                param.pvalue = ptrace.getstr(self._pid, v)
            except UnicodeDecodeError:
                msg = _("failed to collect parameter '{} {}' for {}()")
                raise SyscallParamError(msg.format(t, n, self.name))
        return param

# vim: ts=4 sts=4 sw=4 sta et ai
