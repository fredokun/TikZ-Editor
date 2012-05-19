#!/usr/bin/env python

# Copyright 2012 (C) Mickael Menu <mickael.menu@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program. If not, see <http://www.gnu.org/licenses/>.

# automatically downloads setuptools if needed
import distribute_setup
distribute_setup.use_setuptools()

from setuptools import setup, find_packages

import tikz_editor.globals as globals

setup(
	name = globals.APPLICATION_NAME,
	version = globals.VERSION,
	packages = find_packages(),
	include_package_data = True,
	package_data = {'': ['*.png', '*.html']},

	# metadatas
	author       = globals.AUTHORS,
	author_email = globals.EMAIL,
	description  = globals.APPLICATION_DESCRIPTION,
	license      = "GPL v2",
	keywords     = "tikz code editor latex preview",
	url          = globals.WEBSITE,

	# auto-creates a GUI Python script to launch the application
	entry_points = {'gui_scripts': ['tikz-editor = tikz_editor:start']}
)
