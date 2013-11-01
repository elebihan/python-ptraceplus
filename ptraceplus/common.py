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
Common functions/helpers
"""

import os
import logging
from gettext import bindtextdomain, textdomain

__LOG_LEVELS = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'error': logging.ERROR
}

try:
    __level = __LOG_LEVELS[os.environ.get('PTRACEPLUS_LOG', 'warning')]
except:
    __level = logging.WARNING

__logger = logging.getLogger('ptraceplus')
__logger.setLevel(__level)

def debug(message):
    """Log a debug message.

    The message will only be printed to standard output if the environment
    variable 'PTRACEPLUS_LOG' is set to 'debug'.

    :param message: the message to be logged.
    :type message: str.
    """
    __logger.debug(message)

def setup_i18n():
    """Set up internationalization."""
    root_dir = os.path.dirname(os.path.abspath(__file__))
    if 'lib' not in root_dir:
        return
    root_dir, mod_dir = root_dir.split('lib', 1)
    locale_dir = os.path.join(root_dir, 'share', 'locale')

    bindtextdomain('ptraceplus', locale_dir)
    textdomain('ptraceplus')

# vim: ts=4 sts=4 sw=4 et ai
