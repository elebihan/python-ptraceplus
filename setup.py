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
from distutils.core import setup, Extension
from disthelpers import build, build_trans, build_man, install_data
from ptraceplus import __version__

major, minor, micro = __version__.split('.')

ptraceminus = Extension('ptraceminus',
                        define_macros=[('MAJOR_VERSION', major),
                                       ('MINOR_VERSION', minor)],
                        sources=[os.path.join('ext', 'ptraceminus.c')])

setup(name='python-ptraceplus',
      version=__version__,
      description='Ptrace bindings + extra stuff',
      long_description='''
      Ptrace bindings and extra stuff.
      ''',
      license='GPLv3',
      url='https://github.com/elebihan/python-ptraceplus/',
      platforms=['linux'],
      classifiers=('Programming Language :: Python :: 3',
                   'Intended Audience :: Developers',
                   'Natural Language :: English'
                   'License :: OSI Approved :: GNU General Public License (GPL)',),
      keywords=['ptrace'],
      requires=['docutils (>=0.11)'],
      packages=['ptraceplus'],
      scripts=['scripts/ptraceplus'],
      data_files=[('share/man/man1', ['build/man/man1/ptraceplus.1'])],
      author='Eric Le Bihan',
      author_email='eric.le.bihan.dev@free.fr',
      ext_modules=[ptraceminus],
      cmdclass = {'build': build,
                  'build_man': build_man,
                  'build_trans': build_trans,
                  'install_data': install_data})

# vim: ts=4 sts=4 sw=4 sta et ai
