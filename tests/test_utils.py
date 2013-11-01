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
from ptraceplus import utils
from common import gen_test_progs, DATA_DIR

class TestSpawnChild(unittest.TestCase):

    def setUp(self):
        gen_test_progs()

    def test_spawn(self):
        """Test if local program can be spawned"""
        args = [os.path.join(DATA_DIR, b) for b in ('father', 'child')]
        utils.spawn_child(args)

    def test_spawn_path(self):
        """Test if program can be found in path"""
        utils.find_program('ls')

    def test_spawn_not_found(self):
        """Test if error is raised when child program can not be found"""
        self.assertRaises(utils.SpawnError, utils.spawn_child, ['frob'])

if __name__ == '__main__':
    unittest.main()

# vim: ts=4 sts=4 sw=4 sta et ai
