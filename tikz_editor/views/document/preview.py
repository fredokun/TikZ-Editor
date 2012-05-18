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


class PreviewView(QScrollArea):
	"""
	The preview view displays the preview of the TikZ figure.
	"""

	NORMAL_BACKGROUND_COLOR = "white"
	WAITING_BACKGROUND_COLOR = "#F5F5F5"
	ERROR_BACKGROUND_COLOR = "#FFE8E8"

	def __init__(self, parent=None):
		super(PreviewView, self).__init__(parent)
		self.app_controller = None
		self._figure_view = None
		self.setWidgetResizable(True)
		self.showNormalBackground()

		self.last_cursor_position_x = 0
		self.last_cursor_position_y = 0

	@property
	def figure_view(self):
		return self._figure_view

	@figure_view.setter
	def figure_view(self, figure_view):
		figure_view.setAlignment(Qt.AlignCenter)
		self._figure_view = figure_view
		self.setWidget(figure_view)

	@property
	def figure(self):
		return self.figure_view.pixmap()

	@figure.setter
	def figure(self, image_file_path):
		assert image_file_path is not None
		self.figure_view.setPixmap(QPixmap(image_file_path))

	def showWaitingBackground(self):
		self.setBackgroundColor(PreviewView.WAITING_BACKGROUND_COLOR)

	def showNormalBackground(self):
		self.setBackgroundColor(PreviewView.NORMAL_BACKGROUND_COLOR)

	def showErrorBackground(self):
		self.setBackgroundColor(PreviewView.ERROR_BACKGROUND_COLOR)

	def setBackgroundColor(self, color):
		self.setStyleSheet("QLabel { background-color: %s}" % color)

	def mousePressEvent(self, event):
		# store the current position of cursor
		self.last_cursor_position_x = event.pos().x()
		self.last_cursor_position_y = event.pos().y()

		# hide mouse pointer
		self.parent().setCursor(QCursor(Qt.BlankCursor))

	def mouseReleaseEvent(self, event):
		# show mouse pointer
		self.parent().unsetCursor()

	def mouseMoveEvent(self, event):
		# scroll the figure when the user is dragging it
		x = event.pos().x()
		y = event.pos().y()
		dx = self.last_cursor_position_x - x
		dy = self.last_cursor_position_y - y
		self.scrollBy(dx, dy)
		self.last_cursor_position_x = x
		self.last_cursor_position_y = y

	def scrollBy(self, dx, dy):
		x = self.horizontalScrollBar().value()
		y = self.verticalScrollBar().value()
		self.horizontalScrollBar().setValue(x + dx)
		self.verticalScrollBar().setValue(y + dy)
