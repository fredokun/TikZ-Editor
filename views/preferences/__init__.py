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

from tools.qt import ActionFactory, ToolBarFactory

class PreferencesView(QMainWindow):
	"""
	The preferences window is used to change the user defaults.
	"""
	SHOW_EDITOR_ACTION = "showEditor"
	SHOW_DOCUMENT_ACTION = "showDocument"
	SHOW_PREVIEW_ACTION = "showPreview"
	SHOW_SNIPPETS_ACTION = "showSnippets"
	
	def __init__(self, parent=None):
		super(PreferencesView, self).__init__(parent)
		self.app_controller = None
		self.editor = None
		self.document = None
		self.preview = None
		self.snippets = None
		self.actions = {}
		self.toolbar = None
		self.stacked_widget = None
		self.resize_animation = None
		
	def initView(self):
		self._initWindowProperties()
		self._initToolBar()
		self._initStackedWidgets()
		self._initResizeAnimation()
		self.showEditorPreferences()
		
	def _initWindowProperties(self):
		self.setWindowTitle("Preferences")
		self.setFixedWidth(self.maxWidth())
	
	def _initToolBar(self):
		self.toolbar = ToolBarFactory.createToolBar(self, "Preferences")
		self._initToolBarActions()
	
	def _initToolBarActions(self):
		show_editor_action = ActionFactory.createAction(self.toolbar, "Editor", "Show editor's preferences", shortcut=None, slot=self.showEditorPreferences, checkable=True)
		show_document_action = ActionFactory.createAction(self.toolbar, "Document", "Show document's preferences", shortcut=None, slot=self.showDocumentPreferences, checkable=True)
		show_preview_action = ActionFactory.createAction(self.toolbar, "Preview", "Show preview's preferences", shortcut=None, slot=self.showPreviewPreferences, checkable=True)
		show_snippets_action = ActionFactory.createAction(self.toolbar, "Snippets", "Show snippets preferences", shortcut=None, slot=self.showSnippetsPreferences, checkable=True)
		self.actions[PreferencesView.SHOW_EDITOR_ACTION] = show_editor_action
		self.actions[PreferencesView.SHOW_DOCUMENT_ACTION] = show_document_action
		self.actions[PreferencesView.SHOW_PREVIEW_ACTION] = show_preview_action
		self.actions[PreferencesView.SHOW_SNIPPETS_ACTION] = show_snippets_action
		
		actions_group = QActionGroup(self)
		actions_group.addAction(show_editor_action)
		actions_group.addAction(show_document_action)
		actions_group.addAction(show_preview_action)
		actions_group.addAction(show_snippets_action)
		ToolBarFactory.addItemsToToolBar(
			(None, show_editor_action, show_document_action, show_preview_action, show_snippets_action, None),
			self.toolbar)
		
	def _initStackedWidgets(self):
		self.stacked_widget = QStackedWidget(self)
		self.stacked_widget.addWidget(self.editor)
		self.stacked_widget.addWidget(self.document)
		self.stacked_widget.addWidget(self.preview)
		self.stacked_widget.addWidget(self.snippets)
		self.setCentralWidget(self.stacked_widget)
	
	def _initResizeAnimation(self):
		"""
		The resize animation is used to resize the preferences window to match currently
		displayed view.
		"""
		self.resize_animation = QPropertyAnimation(self, "geometry")
		self.resize_animation.setDuration(150)
		self.resize_animation.finished.connect(self._resizeAnimationFinished)
	
	def _resizeAnimationFinished(self):
		self.setMinimumHeight(self.geometry().height())
		if self.stacked_widget.currentWidget() == self.editor:
			# disable window resizing in editor preferences
			self.setMaximumHeight(self.geometry().height())
	
	def maxWidth(self):
		"""
		Returns the greater width of all sub-views.
		"""
		min_width = 500
		editor_width = self.editor.sizeHint().width()
		document_width = self.document.sizeHint().width()
		preview_width = self.preview.sizeHint().width()
		snippets_width = self.snippets.sizeHint().width()
		return max(min_width, editor_width, preview_width)
	
	def showDocumentPreferences(self):
		self.stacked_widget.setCurrentWidget(self.document)
		if not self.actions[PreferencesView.SHOW_DOCUMENT_ACTION].isChecked():
			self.actions[PreferencesView.SHOW_DOCUMENT_ACTION].setChecked(True)
		self._resizeHeightToMatchCurrentView()
		
	def showEditorPreferences(self):
		self.stacked_widget.setCurrentWidget(self.editor)
		if not self.actions[PreferencesView.SHOW_EDITOR_ACTION].isChecked():
			self.actions[PreferencesView.SHOW_EDITOR_ACTION].setChecked(True)
		self._resizeHeightToMatchCurrentView()
	
	def showPreviewPreferences(self):
		self.stacked_widget.setCurrentWidget(self.preview)
		if not self.actions[PreferencesView.SHOW_PREVIEW_ACTION].isChecked():
			self.actions[PreferencesView.SHOW_PREVIEW_ACTION].setChecked(True)
		self._resizeHeightToMatchCurrentView()
	
	def showSnippetsPreferences(self):
		self.stacked_widget.setCurrentWidget(self.snippets)
		if not self.actions[PreferencesView.SHOW_SNIPPETS_ACTION].isChecked():
			self.actions[PreferencesView.SHOW_SNIPPETS_ACTION].setChecked(True)
		self._resizeHeightToMatchCurrentView()
		
	def _resizeHeightToMatchCurrentView(self):
		if self.resize_animation.state() is not QPropertyAnimation.Stopped:
			self.resize_animation.stop()
		current_view = self.stacked_widget.currentWidget()
		geometry = self.geometry()
		previous_height = geometry.height()
		self.resize_animation.setStartValue(geometry)
		view_height = current_view.sizeHint().height()
		toolbar_height = self.toolbar.sizeHint().height()
		total_height = view_height + toolbar_height
		geometry.setHeight(total_height)
		self.setMinimumHeight(min(previous_height, total_height))
		self.setMaximumHeight(2000)
		self.resize_animation.setEndValue(geometry)
		self.resize_animation.start()