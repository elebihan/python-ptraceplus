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
Collects information about a system call (Linux, x86)
"""

from .names import SYSCALL_NAMES
from ..prototypes import SYSCALL_PROTOS
from ...core import Syscall

class SyscallLinux(Syscall):

    def _get_name(self):
        return SYSCALL_NAMES[self.num]

    def _get_proto(self):
        return SYSCALL_PROTOS[self.name]

    def _get_result_from_regs(self, regs):
        return regs['eax']

    def _get_params_from_regs(self, regs):
        values = (regs['ebx'], regs['ecx'], regs['edx'],
                  regs['esi'], regs['edi'], regs['ebp'])
        return [v & 0xffffffff for v in values]

# vim: ts=4 sts=4 sw=4 sta et ai
