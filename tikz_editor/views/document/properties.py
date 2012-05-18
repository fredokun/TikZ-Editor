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

from PyQt4.QtCore import *
from PyQt4.QtGui import *


class TestWidget(QWidget):
	def __init__(self, parent=None):
		super(TestWidget, self).__init__(parent)

		s = QStackedWidget()
		s.addWidget(QLabel("Property Page 1"))
		s.addWidget(QLabel("Property Page 2"))
		s.addWidget(QLabel("Property Page 3"))

		p = QComboBox()
		p.addItem("Property Page 1")
		p.addItem("Property Page 2")
		p.addItem("Property Page 3")

		self.connect(p, SIGNAL("activated(int)"), s, SLOT("setCurrentIndex(int)"))

		l = QVBoxLayout()
		l.addWidget(p)
		l.addWidget(s)
		self.setLayout(l)


class PropertiesView(QDockWidget):
	"""
	The property view shows the properties of TikZ objects.
	This view is not used at the moment, it should be displayed as a dock on the
	document window.
	"""
	def __init__(self, parent=None):
		super(PropertiesView, self).__init__("Object Properties", parent)
		self.app_controller = None

		# dock widget configuration
		self.setObjectName("ObjectPropertiesWidget")
		self.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
		self.setFeatures(QDockWidget.DockWidgetMovable)

		# add the view as a dock to parent window
		parent.addDockWidget(Qt.RightDockWidgetArea, self)

		self.setWidget(TestWidget())

	def initView(self):
		pass
