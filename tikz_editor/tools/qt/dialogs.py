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
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class Dialogs(object):
	"""
	Dialogs is a wrapper to QT's dialogs
	"""
	SAVE = 1
	DISCARD = 2
	CANCEL = 3

	@staticmethod
	def closeDialog(title, text, parent_view=None):
		dialog = QMessageBox(parent_view)
		dialog.setText(title)
		dialog.setInformativeText(text)
		dialog.setStandardButtons(QMessageBox.Discard | QMessageBox.Save | QMessageBox.Cancel)
		dialog.setDefaultButton(QMessageBox.Save)
		dialog.setWindowModality(Qt.WindowModal)
		response = dialog.exec_()
		ret = Dialogs.CANCEL
		if response == QMessageBox.Save:
			ret = Dialogs.SAVE
		elif response == QMessageBox.Discard:
			ret = Dialogs.DISCARD
		return ret

	@staticmethod
	def askQuestion(title, question, parent_view=None):
		answer = QMessageBox.question(parent_view, title, question, QMessageBox.Yes | QMessageBox.No)
		return answer == QMessageBox.Yes

	@staticmethod
	def showError(error_message):
		if isinstance(error_message, Exception):
			import logging
			logging.exception(error_message)
			error_message = str(error_message)
		QMessageBox.critical(None, "Error", error_message)

	@staticmethod
	def selectFont(base_font=None):
		(selected_font, is_selected) = QFontDialog.getFont(base_font)
		if not is_selected:
			selected_font = None
		return selected_font
