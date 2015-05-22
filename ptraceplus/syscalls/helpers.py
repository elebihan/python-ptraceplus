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
Syscall handling helpers (platform abstraction)
"""

import platform
from gettext import gettext as _

if platform.system() == 'Linux':
    if platform.machine() in ('i386', 'i486', 'i586', 'i686'):
        from .linux.x86.names import SYSCALL_NAMES
        from .linux.x86.syscall import SyscallLinux as Syscall
    elif platform.machine() in ('x86_64'):
        from .linux.x86_64.names import SYSCALL_NAMES
        from .linux.x86_64.syscall import SyscallLinux as Syscall
    else:
        raise RuntimeError(_('Unsupported architecture'))
else:
    raise RuntimeError(_('Unsupported system'))


def convert_names(names):
    return [k for k, v in SYSCALL_NAMES.items() if v in names]


def create_syscall(pid):
    return Syscall(pid)


def format_syscall(syscall, detailed=False):
    if detailed:
        values = [str(p) for p in syscall.params]
        params = '(' + ', '.join(values) + ')'
    else:
        params = '()'
    return "{}{}".format(syscall.name, params)


# vim: ts=4 sts=4 sw=4 sta et ai
