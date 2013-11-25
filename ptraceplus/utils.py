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
Utilities
"""

import sys
import os
import signal
import ptraceminus as ptrace
from gettext import gettext as _
from .common import debug

try:
    __MAXFD = os.sysconf('SC_OPEN_MAX')
except:
    __MAXFD = 256

class SpawnError(Exception):
    """Error raised when child can not be spawned"""

def find_program(program):
    """Try to find a program in $PATH.

    :param program: name of the program.
    :type program: str.

    :returns: full path to the program.
    :rtype str.
    """
    if os.path.isabs(program):
        return program
    if os.path.dirname(program):
        return os.path.normpath(os.path.join(os.getcwd(), program))
    for path in os.environ['PATH'].split(':'):
        filename = os.path.join(path, program)
        if os.access(filename, os.X_OK):
            return filename
    raise SpawnError(_('Program not found'))

def spawn_child(arguments, env=None, quiet=True):
    """Spawn a child process.

    :param arguments: arguments of the child program.
    :type arguments: list of str.

    :param env: environment variables for child program.
    :type env: mapping between strings

    :returns: PID of the child program.
    :rtype: int.
    """
    program = find_program(arguments[0])
    arguments[0] = program
    pid = os.fork()
    if pid:
        debug(_("Spawned process {}").format(pid))
        return pid
    else:
        try:
            ptrace.traceme()
        except ptrace.PtraceError as e:
            raise SpawnError(_("Failed to trace child process {}").format(e))

        for fd in range(3, __MAXFD):
            try:
                os.close(fd)
            except OSError:
                pass

        if quiet:
            try:
                null = open(os.devnull, 'wb')
                os.dup2(null.fileno(), 1)
                os.dup2(1, 2)
                null.close()
            except IOError:
                os.close(2)
                os.close(1)

        os.kill(os.getpid(), signal.SIGSTOP)

        try:
            if env:
                os.execve(arguments[0], arguments, env)
            else:
                os.execv(arguments[0], arguments)
        except:
            sys.exit(255)

# vim: ts=4 sts=4 sw=4 sta et ai
