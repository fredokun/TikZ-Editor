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

from PyQt5.QtCore import *
import tikz_editor.resources
from tikz_editor.tools import File


class AboutController(QObject):
	"""
	Controller for the "About" dialog.
	"""

	def __init__(self):
		super(AboutController, self).__init__()
		self.view = None
		self.app_controller = None

	def initController(self):
		self.view.setImage(":/icon_about.png")
		self.view.setInfoHTML(File.readContentFromFilePath(":/about.html"))

	def showAbout(self):
		self.view.show()
		self.view.raise_()
