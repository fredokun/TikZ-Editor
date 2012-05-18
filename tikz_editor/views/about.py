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

import tikz_editor.globals as globals


class AboutView(QMainWindow):
	"""
	About window.
	"""
	def __init__(self, parent=None):
		super(AboutView, self).__init__(parent)
		self.app_controller = None
		self.image = QLabel()
		self.title_label = QLabel("<center><h3>TikZ Editor</h3></center>")
		version = globals.VERSION
		if globals.GIT_VERSION != u'':
			version += ' (%s)' % globals.GIT_VERSION
		self.version_label = QLabel("<center><small>Version %s</small></center>" % version)
		self.copyright_label = QLabel("<center><small>Copyright 2012 %s</small></center>" % globals.AUTHORS)
		self.info_text = QTextEdit()

	def initView(self):
		self.image.setAlignment(Qt.AlignCenter)
		self.info_text.setReadOnly(True)
		self._initWindowProperties()
		self._initLayout()

	def setInfoHTML(self, content):
		self.info_text.setText(content)

	def setImage(self, path):
		self.image.setPixmap(QPixmap(path))

	def _initWindowProperties(self):
		self.setWindowTitle("About TikZ Editor")
		self.setFixedWidth(300)
		self.setFixedHeight(350)

	def _initLayout(self):
		content = QWidget()
		layout = QVBoxLayout()
		layout.setContentsMargins(0, 10, 0, 10)
		layout.addWidget(self.image)
		layout.addWidget(self.title_label)
		layout.addWidget(self.version_label)
		layout.addWidget(self.info_text)
		layout.addWidget(self.copyright_label)
		content.setLayout(layout)
		self.setCentralWidget(content)
