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

import tikz_editor.globals.actions as actions
from tikz_editor.models import Preferences
from tikz_editor.tools.qt import ActionFactory, ToolBarFactory

LOGS_VIEW = 0
ERRORS_VIEW = 1


class FeedbackView(QMainWindow):
	"""
	The feedback view displays the pdf2image converter error and logs views.
	"""

	SHOW_ERRORS_ACTION = "showError"
	SHOW_LOGS_ACTION = "showLogs"

	def __init__(self, parent=None):
		super(QMainWindow, self).__init__(parent)
		self.app_controller = None
		self.errors_view = None
		self.logs_view = None
		self.stacked_widget = None
		self.actions = {}

	def initView(self):
		self._initToolBar()
		self._initStackedWidgets()
		self._initSelectedView()

	def _initToolBar(self):
		toolbar = ToolBarFactory.createToolBar(self, "Feedback")
		self._initToolBarActions(toolbar)

	def _initToolBarActions(self, toolbar):
		actions_group = QActionGroup(self)
		show_logs_action = ActionFactory.createAction(toolbar, "Logs", "Show LaTeX preview logs", shortcut="Ctrl+L", slot=self.showLogsView, checkable=True)
		show_errors_action = ActionFactory.createAction(toolbar, "Errors", "Show LaTeX preview errors", shortcut="Ctrl+E", slot=self.showErrorsView, checkable=True)
		self.actions[actions.SHOW_LOGS] = show_logs_action
		self.actions[actions.SHOW_ERRORS] = show_errors_action

		actions_group.addAction(show_logs_action)
		actions_group.addAction(show_errors_action)
		ToolBarFactory.addItemsToToolBar((None, show_logs_action, show_errors_action, QLabel()), toolbar)

	def _initStackedWidgets(self):
		self.stacked_widget = QStackedWidget(self)
		self.stacked_widget.addWidget(self.logs_view)
		self.stacked_widget.addWidget(self.errors_view)
		self.setCentralWidget(self.stacked_widget)

	def _initSelectedView(self):
		selected_view = Preferences.getSelectedFeedbackView()
		if selected_view == ERRORS_VIEW:
			self.showErrorsView()
		else:
			self.showLogsView()

	def showLogsView(self):
		self.stacked_widget.setCurrentWidget(self.logs_view)
		Preferences.setSelectedFeedbackView(LOGS_VIEW)
		if not self.actions[actions.SHOW_LOGS].isChecked():
			self.actions[actions.SHOW_LOGS].setChecked(True)

	def showErrorsView(self):
		self.stacked_widget.setCurrentWidget(self.errors_view)
		Preferences.setSelectedFeedbackView(ERRORS_VIEW)
		if not self.actions[actions.SHOW_ERRORS].isChecked():
			self.actions[actions.SHOW_ERRORS].setChecked(True)
