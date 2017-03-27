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

from tikz_editor.models import Preferences
import tikz_editor.globals.actions as actions
from tikz_editor.tools.qt import ActionFactory, ToolBarFactory


class ContentView(QMainWindow):
	"""
	The content view displays the source and preamble editors.
	"""
	def __init__(self, parent=None):
		super(QMainWindow, self).__init__(parent)
		self.app_controller = None
		self.source_editor_view = None
		self.preamble_editor_view = None
		self.stacked_widget = None
		self.actions = {}

	@property
	def current_editor_view(self):
		return self.stacked_widget.currentWidget()

	@current_editor_view.setter
	def current_editor_view(self, view):
		self.stacked_widget.setCurrentWidget(view)
		view.setFocus()

	def initView(self):
		self.source_editor_view.cursorPositionChanged.connect(self._sourceCursorPositionChanged)
		self.source_editor_view.selectionChanged.connect(self._sourceSelectionChanged)
		self.source_editor_view.modificationAttempted.connect(self._sourceModificationAttemptedWhileReadOnly)
		self._initToolBar()
		self._initStackedWidgets()

	def _initToolBar(self):
		toolbar = ToolBarFactory.createToolBar(self, "Content")
		self._initToolBarActions(toolbar)

	def _initToolBarActions(self, toolbar):
		actions_group = QActionGroup(self)
                show_source_action = ActionFactory.createAction(toolbar, "Source", "Show LaTeX source editor", slot=self.showSourceView, checkable=True)
                show_preamble_action = ActionFactory.createAction(toolbar, "Preamble", "Show LaTeX preamble editor", slot=self.showPreambleView, checkable=True)

		self.actions[actions.SHOW_SOURCE] = show_source_action
		self.actions[actions.SHOW_PREAMBLE] = show_preamble_action

		show_source_action.setChecked(True)
		actions_group.addAction(show_source_action)
		actions_group.addAction(show_preamble_action)

		ToolBarFactory.addItemsToToolBar((
			self.app_controller.actions[actions.PREVIEW],
			("Copy", self.app_controller.actions[actions.COPY_MENU]),
			("Snippets", self.app_controller.actions[actions.SNIPPETS_MENU]),
			None, show_source_action, show_preamble_action,
			QLabel()), toolbar)

	def _initStackedWidgets(self):
		self.stacked_widget = QStackedWidget(self)
		self.stacked_widget.addWidget(self.source_editor_view)
		self.stacked_widget.addWidget(self.preamble_editor_view)
		self.setCentralWidget(self.stacked_widget)

	def showSourceView(self):
		self.current_editor_view = self.source_editor_view
		if not self.actions[actions.SHOW_SOURCE].isChecked():
			self.actions[actions.SHOW_SOURCE].setChecked(True)

	def showPreambleView(self):
		self.current_editor_view = self.preamble_editor_view
		if not self.actions[actions.SHOW_PREAMBLE].isChecked():
			self.actions[actions.SHOW_PREAMBLE].setChecked(True)

	def toggleViews(self):
		if self.current_editor_view is self.source_editor_view:
			self.showPreambleView()
		else:
			self.showSourceView()

	def _sourceModificationAttemptedWhileReadOnly(self):
		source = self.source_editor_view
		(line, index) = source.getCursorPosition()
		if (line > 0 and line < source.lines() - 1) or line == 0 and index > 18:
			source.setReadOnly(False)
		else:
			# fire system alert sound
			QApplication.beep()

	def _sourceCursorPositionChanged(self, line, index):
		select_tags = Preferences.getSelectTags()
		if(not select_tags):
			source = self.source_editor_view
			content = source.content
			if not (content.startswith("\\begin{tikzpicture}") and content.startswith("\\begin{tikzpicture")):
				source.content = "\\begin{tikzpicture}" + content[18:]
			if line == 0 and index < 20:
				source.setCursorPosition(0, 19)
				source.setReadOnly(True)
			elif line == source.lines() - 1:
				source.setCursorPosition(source.lines() - 2, source.lineSize(source.lines() - 1))
				source.setReadOnly(True)

	def _sourceSelectionChanged(self):
		select_tags = Preferences.getSelectTags()
		if(not select_tags):
			source = self.source_editor_view
			(line_from, index_from, line_to, index_to) = source.getSelection()
			selection_changed = False
			if line_from == 0 and index_from < 19:
				index_from = 19
				selection_changed = True
			if line_to == source.lines() - 1:
				line_to = source.lines() - 2
				index_to = source.lineSize(line_to + 1)
				selection_changed = True
			if selection_changed:
				source.setSelection(line_from, index_from, line_to, index_to)
