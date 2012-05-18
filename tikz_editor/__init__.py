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

import os
import sys
import atexit # necessary for pyinstaller deployment
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from tikz_editor.controllers import ControllerFactory
from tikz_editor.tools import isMacintoshComputer
import tikz_editor.globals as globals


def start():
	app = QApplication(sys.argv)
	app.setOrganizationName(globals.ORGANIZATION_NAME)
	app.setOrganizationDomain(globals.ORGANIZATION_DOMAIN)
	app.setApplicationName(globals.APPLICATION_NAME)

	if isMacintoshComputer():
		# add /opt/local/bin to PATH to find pdflatex binary -- useful for Mac plateform using Macports
		os.environ['PATH'] = os.environ.get('PATH', '/usr/bin') + ':/opt/local/bin'
		app.setQuitOnLastWindowClosed(False)

	app_controller = ControllerFactory.createAppController()

	args = app.arguments()[1:]
	if len(args) > 0:
		for file_path in args:
			app_controller.open(file_path)
	else:
		app_controller.new()

	app.exec_()
	app_controller.quit()
