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

import os
import unittest
from ptraceplus.tracer import Tracer
from common import gen_test_progs, DATA_DIR


class TestTracerBasic(unittest.TestCase):
    """Basic Tracer tests"""

    def setUp(self):
        self._tracer = Tracer()

    def test_no_processes(self):
        """Test if tracer has no process"""
        self.assertFalse(self._tracer.has_processes)

    def test_set_trace_options(self):
        """Test if trace options can be set"""
        self._tracer.fork_enabled = True
        self._tracer.exec_enabled = True
        self._tracer.sysgood_enabled = True

    def tearDown(self):
        self._tracer.quit()


class TestTracerSpawn(unittest.TestCase):
    """Process spawing tests"""

    def setUp(self):
        gen_test_progs()
        self._tracer = Tracer()

    def test_add_process(self):
        args = [os.path.join(DATA_DIR, p) for p in ('father', 'child')]
        self._tracer.spawn_process(args)

    def tearDown(self):
        self._tracer.quit()

if __name__ == '__main__':
    unittest.main()

# vim: ts=4 sts=4 sw=4 sta et ai
