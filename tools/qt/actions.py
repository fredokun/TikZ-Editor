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

from PyQt4.QtGui import *
from PyQt4.QtCore import *

class ActionFactory(object):
	"""
	Helper functions to create Qt actions
	"""

	@staticmethod
	def createAction(parent, text, tip=None, shortcut=None, slot=None, checkable=False, icon=None):
		a = QAction(text, parent)
		if icon is not None:
			a.setIcon(QIcon(":/%s.png" % icon))
		if shortcut is not None:
			a.setShortcut(shortcut)
		if tip is not None:
			a.setToolTip(tip)
			a.setStatusTip(tip)
		if slot is not None:
			a.triggered.connect(slot)
		if checkable:
			a.setCheckable(True)
		return a
		
	@staticmethod
	def addActionsToMenu(actions, menu):
		for action in actions:
			if action is None:
				menu.addSeparator()
			else:
				menu.addAction(action)