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
Collections of tracers
"""

from .tracerplus import TracerPlus
from .syscalls.helpers import format_syscall, convert_names
from gettext import gettext as _

class TracerStats:
    __slots__ = ['n_procs', 'results']

    def __init__(self, n, r):
        self.n_procs = n
        self.results = r

class SyscallTracer(TracerPlus):
    def __init__(self, args, verbose=False):
        TracerPlus.__init__(self, args)
        self._verbose = verbose
        self._results = {}
        self._selection = []

    @property
    def stats(self):
        results = [(n, c) for n, c in self._results.items()]
        return TracerStats(self.n_procs, sorted(results))

    def filter_syscalls(self, names):
        self._selection = convert_names(names)

    def _on_event(self, event):
        if self._verbose:
            print(event)

    def _on_syscall_enter(self, syscall):
        if self._verbose or syscall.num in self._selection:
            syscall.collect_params()
        if self._verbose:
            txt = "[{}] {} = ?"
            print(txt.format(syscall.pid, format_syscall(syscall, True)))

    def _on_syscall_exit(self, syscall):
        if self._verbose or syscall.num in self._selection:
            res = syscall.collect_result()
            if not syscall.name in self._results:
                self._results[syscall.name] = 0
            else:
                self._results[syscall.name] += 1
            txt = "[{}] {} = {}"
            print(txt.format(syscall.pid, format_syscall(syscall, True), res))

def format_tracer_stats(stats):
    print("----")
    print(_("Number of processes traced: {}").format(stats.n_procs))
    if stats.results:
        print(_("Syscalls statistics:"))
    for n, c in stats.results:
        print(" {:<24}: {}".format(n, c))


# vim: ts=4 sts=4 sw=4 sta et ai
