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

import os
from .tracerplus import TracerPlus
from .syscalls.helpers import format_syscall, convert_names
from gettext import gettext as _

class TracerStats:
    __slots__ = ['n_traced', 'n_filtered', 'results']

    def __init__(self, nt, nf, r):
        self.n_traced = nt
        self.n_filtered = nf
        self.results = r

class SyscallTracer(TracerPlus):
    def __init__(self, args, quiet=True, full=False, stream=None):
        TracerPlus.__init__(self, args, quiet=quiet)
        self._os = stream
        self._full = full
        self._results = {}
        self._syscalls = []
        self._pids = []
        self._progs = []

    @property
    def stats(self):
        results = [(n, c) for n, c in self._results.items()]
        return TracerStats(self.n_procs, len(self._progs), sorted(results))

    def filter_syscalls(self, names):
        self._syscalls = convert_names(names)

    def filter_programs(self, names):
        for name in names:
            self._progs.append(name)

    def _check_wanted_syscall(self, syscall):
        if self._progs:
            if syscall.pid in self._pids:
                if self._syscalls:
                    if syscall.num in self._syscalls:
                        return True
                    else:
                        return False
                else:
                    return True
            else:
                return False
        else:
            if self._syscalls:
                if syscall.num in self._syscalls:
                    return True
                else:
                    return False
            else:
                return True

    def _log(self, message):
        if self._os:
            self._os.write(message + '\n')
        else:
            print(message)

    def _on_event(self, event):
        if self._full:
            self._log(str(event))

    def _on_syscall_enter(self, syscall):
        if syscall.name == 'execve':
            params = syscall.collect_params()
            for name in self._progs:
                if params[0].pvalue.endswith(name):
                    self._pids.append(syscall.pid)

        wanted = self._check_wanted_syscall(syscall)

        if self._full or wanted:
            if not syscall.params:
                syscall.collect_params()
        if self._full:
            txt = "[{}] {} = ?"
            self._log(txt.format(syscall.pid, format_syscall(syscall, True)))

    def _on_syscall_exit(self, syscall):
        wanted = self._check_wanted_syscall(syscall)
        if self._full or wanted:
            res = syscall.collect_result()
            if not syscall.name in self._results:
                self._results[syscall.name] = 0
            else:
                self._results[syscall.name] += 1
            txt = "[{}] {} = {}"
            self._log(txt.format(syscall.pid, format_syscall(syscall, True), res))

def format_tracer_stats(stats):
    print("----")
    print(_("Number of processes traced: {}").format(stats.n_traced))
    print(_("Number of processes filtered: {}").format(stats.n_filtered))
    if stats.results:
        print(_("Syscalls statistics:"))
    for n, c in stats.results:
        print(" {:<24}: {}".format(n, c))


def format_process_info(info, with_files=True):
        text = " - pid: {}\n".format(info.pid)
        text += "   ppid: {}\n".format(info.ppid)
        text += "   cmd: {}\n".format(' '.join(info.args))
        if with_files:
            text += "   read:\n"
            for f in set(info.rfiles):
                text += "     - {}\n".format(f)
            text += "   write:\n"
            for f in set(info.wfiles):
                text += "     - {}\n".format(f)
        text += "   code: {}\n".format(info.code)
        return text

class ProcessInfo:
    def __init__(self, pid, ppid=0):
        self.pid = pid
        self.ppid = ppid
        self.args = []
        self.rfiles = []
        self.wfiles = []
        self.code = 0
        self.fname = None
        self.faccess = None
        self.allowed = False

class ExecutionTracer(TracerPlus):
    def __init__(self, args, quiet=True, stream=None):
        TracerPlus.__init__(self, args, quiet=quiet)
        self._os = stream
        self._progs = []
        self._infos = {}
        self.with_files = False

    def filter_programs(self, names):
        for name in names:
            self._progs.append(name)

    def _log(self, message):
        if self._os:
            self._os.write(message + '\n')
        else:
            print(message)

    def _on_tracing_started(self, proc):
        self._infos[proc.pid] = ProcessInfo(proc.pid, -1)

    def _on_fork(self, event):
        try:
            info = self._infos[event.child_pid]
            info.ppid = event.pid
        except KeyError:
            info = ProcessInfo(event.child_pid, event.pid)
            self._infos[event.child_pid] = info

    def _on_syscall_enter(self, syscall):
        if syscall.name == 'execve':
            params = syscall.collect_params()
            prog = params[0].pvalue
            if self._progs:
                allowed = False
                for name in self._progs:
                    if prog.endswith(name):
                       allowed = True
                       break
            else:
                allowed = True

            try:
                info = self._infos[syscall.pid]
            except KeyError:
                info = ProcessInfo(syscall.pid)
                self._infos[syscall.pid] = info
            info.allowed = allowed
            info.args = [prog]

        elif syscall.name == 'open' and self.with_files:
            info = self._infos[syscall.pid]
            if info.allowed:
                params = syscall.collect_params()
                info.fname = params[0].pvalue
                info.faccess =  params[1].value

    def _on_syscall_exit(self, syscall):
        if syscall.name == 'open' and self.with_files:
            info = self._infos[syscall.pid]
            if info.allowed:
                result = syscall.collect_result()
                if result > 0:
                    if info.faccess & os.O_WRONLY or info.faccess & os.O_RDWR:
                        info.wfiles.append(info.fname)
                    else:
                        info.rfiles.append(info.fname)

    def _on_exit(self, event):
        info = self._infos[event.pid]
        info.code = event.code
        if info.allowed and info.args:
            self._log(format_process_info(info, self.with_files))
        del self._infos[event.pid]

# vim: ts=4 sts=4 sw=4 sta et ai
