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

import sys
import argparse
import logging
from ptraceplus import __version__
from ptraceplus.common import setup_i18n
from ptraceplus.extra import SyscallTracer, format_tracer_stats
from ptraceplus.extra import ExecutionTracer
from gettext import gettext as _

logging.basicConfig()

setup_i18n()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--version',
                        action='version',
                        version=__version__)
    parser.add_argument('arguments',
                        nargs=argparse.REMAINDER,
                        help=_('arguments of the program'))
    parser.add_argument('--execution', '-x',
                        action='store_true',
                        dest='exec_only',
                        default=False,
                        help=_('trace only execution'))
    parser.add_argument('--args', '-a',
                        action='store_true',
                        dest='with_args',
                        default=False,
                        help=_('get arguments during execution'))
    parser.add_argument('--files', '-f',
                        action='store_true',
                        dest='with_files',
                        default=False,
                        help=_('trace file access during execution'))
    parser.add_argument('--stats', '-s',
                        action='store_true',
                        dest='with_stats',
                        default=False,
                        help=_('compute some statistics'))
    parser.add_argument('--full', '-F',
                        action='store_true',
                        default=False,
                        help=_('trace all events'))
    parser.add_argument('--output', '-o',
                        metavar='FILE',
                        help=_('set output file'))
    parser.add_argument('--syscall', '-S',
                        metavar='NAME',
                        action='append',
                        dest='syscalls',
                        default=[],
                        help=_('filter syscall by name'))
    parser.add_argument('--program', '-P',
                        metavar='NAME',
                        action='append',
                        dest='programs',
                        default=[],
                        help=_('filter program by name'))
    args = parser.parse_args()

    if len(args.arguments) == 0:
        parser.error(_('Missing argument(s)'))

    try:
        if args.output:
            output = open(args.output, 'w')
            quiet = False
        else:
            output = sys.stdout
            quiet = True
    except Exception as err:
        print(_("Error: {}").format(err), file=sys.stderr)
        sys.exit(1)

    try:
        if args.exec_only:
            tracer = ExecutionTracer(args.arguments,
                                     quiet,
                                     output)
            tracer.with_files = args.with_files
            tracer.with_args = args.with_args
        else:
            tracer = SyscallTracer(args.arguments,
                                   quiet,
                                   args.full,
                                   output)
            tracer.filter_syscalls(args.syscalls)
        tracer.filter_programs(args.programs)
        tracer.run()
    finally:
        if output is not sys.stdout:
            output.close()

    if args.with_stats and not args.exec_only:
        print(format_tracer_stats(tracer.stats))

# vim: ts=4 sts=4 sw=4 sta et ai
