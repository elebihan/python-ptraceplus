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
import subprocess

_TEST_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(_TEST_DIR, 'data')

def gen_test_progs():
    with open(os.devnull) as f:
        subprocess.call(['make', '-C', DATA_DIR], stdout=f, stderr=f)

# vim: ts=4 sts=4 sw=4 sta et ai
