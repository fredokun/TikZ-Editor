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
from PyQt5.QtWidgets import *


class ErrorListItem(QListWidgetItem):
	def __init__(self, error, parent=None):
		super(ErrorListItem, self).__init__(str(error), parent)
		self.error = error


class ErrorsView(QListWidget):
	"""
	The errors view displays the list of pdf2image converter errors.
	"""
	errorSelectedSignal = pyqtSignal(object)

	def __init__(self, parent=None):
		super(ErrorsView, self).__init__(parent)
		self.app_controller = None

	def initView(self):
		self.itemClicked.connect(self.errorSelected)

	def clearErrors(self):
		self.clear()

	def addError(self, error):
		ErrorListItem(error, self)

	def errorSelected(self, error_list_item):
		self.errorSelectedSignal.emit(error_list_item.error)
