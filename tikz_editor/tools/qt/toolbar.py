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


class ToolBarFactory(object):
	"""
	Helper functions to create Qt toolbars
	"""

	@staticmethod
	def createToolBar(parent, name):
		toolbar = QToolBar(name, parent)
		toolbar.setMovable(False)
		toolbar.setFloatable(False)
		parent.addToolBar(Qt.TopToolBarArea, toolbar)
		return toolbar

	@staticmethod
	def addItemsToToolBar(items, toolbar):
		for item in items:
			if item is None:
				ToolBarFactory.addSpacerToToolBar(toolbar)
			elif isinstance(item, QAction):
				toolbar.addAction(item)
			elif isinstance(item, tuple):
				ToolBarFactory.addMenuToToolBar(item[0], item[1], toolbar)
			elif isinstance(item, QWidget):
				toolbar.addWidget(item)

	@staticmethod
	def addSpacerToToolBar(toolbar):
		spacer = QWidget()
		spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		toolbar.addWidget(spacer)

	@staticmethod
	def addMenuToToolBar(title, menu, toolbar):
		button = QToolButton()
		button.setToolButtonStyle(Qt.ToolButtonTextOnly)
		button.setDefaultAction(QAction(title, button))
		button.setMenu(menu)
		button.setPopupMode(QToolButton.InstantPopup)
		toolbar.addWidget(button)
