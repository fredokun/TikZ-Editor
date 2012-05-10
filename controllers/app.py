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

import os

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import globals.actions as actions
from models import Preferences
from views import DocumentView
from views.editor import EditorView
from tools import addToClipboard, isMacintoshComputer
from tools import File, TemporaryDirectory
from tools.qt import ActionFactory, Dialogs

class AppController(QObject):
	"""
	The application controller is directing all the user actions to sub-controllers.
	"""
	
	def __init__(self):
		super(AppController, self).__init__()
		self.about_controller = None
		self.documents_controller = None
		self.preferences_controller = None
		self.actions = {}
		self.menu_bar = None
	
	def initController(self):
		self._createActions()
		self._createMenuBar()

	def _createActions(self):
		self.actions[actions.ABOUT] = ActionFactory.createAction(self, "About", "About the application", None, self.about)
		self.actions[actions.CLOSE] = ActionFactory.createAction(self, "Close", "Close the window", QKeySequence.Close, self.close)
		self.actions[actions.COPY] = ActionFactory.createAction(self, "Copy", "Copy selected item", QKeySequence.Copy, self.copy)
		self.actions[actions.COPY_SOURCE] = ActionFactory.createAction(self, "Copy Source", "Copy the TikZ source", "Ctrl+Shift+C", self.copySource)
		self.actions[actions.COPY_PREAMBLE] = ActionFactory.createAction(self, "Copy Preamble", "Copy the preamble", "Ctrl+Shift+P", self.copyPreamble)
		self.actions[actions.COPY_PREAMBLE_AND_SOURCE] = ActionFactory.createAction(self, "Copy Preamble and Source", "Copy the TikZ source with preamble", None, self.copyPreambleAndSource)
		self.actions[actions.CUT] = ActionFactory.createAction(self, "Cut", "Cut selected item", QKeySequence.Cut, self.cut)
		self.actions[actions.NEW] = ActionFactory.createAction(self, "New", "Create a new document", QKeySequence.New, self.new)
		self.actions[actions.OPEN] = ActionFactory.createAction(self, "Open", "Open an existing document", QKeySequence.Open, self.open)
		self.actions[actions.PASTE] = ActionFactory.createAction(self, "Paste", "Paste content of clipboard", QKeySequence.Paste, self.paste)
		self.actions[actions.PREFERENCES] = ActionFactory.createAction(self, "Preferences", "Show the preferences window", QKeySequence.Preferences, self.showPreferences)
		self.actions[actions.PREFERENCES].setMenuRole(QAction.PreferencesRole)
		self.actions[actions.PREVIEW] = ActionFactory.createAction(self, "Preview", "Preview the document", QKeySequence.Print, self.preview)
		self.actions[actions.REDO] = ActionFactory.createAction(self, "Redo", "Redo last action", QKeySequence.Redo, self.redo)
		self.actions[actions.QUIT] = ActionFactory.createAction(self, "Quit", "Quit the application", QKeySequence.Quit, self.quit)
		self.actions[actions.SAVE] = ActionFactory.createAction(self, "Save", "Save the document", QKeySequence.Save, self.save)
		self.actions[actions.SAVE_ALL] = ActionFactory.createAction(self, "Save All", "Save all documents", None, self.saveAll)
		self.actions[actions.SAVE_AS] = ActionFactory.createAction(self, "Save As...", "Save the document as...", QKeySequence.SaveAs, self.saveAs)
		self.actions[actions.UNDO] = ActionFactory.createAction(self, "Undo", "Undo last action", QKeySequence.Undo, self.undo)
	
	def _createMenuBar(self):
		self.menu_bar = QMenuBar()
		self._createFileMenu()
		self._createEditMenu()
		
		# set menu bar of about and preferences windows if we're not on Mac OS X
		if not isMacintoshComputer():
			self.preferences_controller.view.setMenuBar(self.menu_bar)
			self.about_controller.view.setMenuBar(self.menu_bar)

	
	def _createFileMenu(self):
		file_menu = self.menu_bar.addMenu("File")
		ordered_actions = (
			self.actions[actions.NEW],
			self.actions[actions.OPEN],
			None,
			self.actions[actions.CLOSE],
			self.actions[actions.SAVE],
			self.actions[actions.SAVE_AS],
			self.actions[actions.SAVE_ALL],
			None,
			self.actions[actions.PREVIEW],
			None,
			self.actions[actions.ABOUT],
			self.actions[actions.PREFERENCES],
			self.actions[actions.QUIT]
		)
		ActionFactory.addActionsToMenu(ordered_actions, file_menu)
	
	def _createEditMenu(self):
		edit_menu = self.menu_bar.addMenu("Edit")
		ordered_actions = (
			self.actions[actions.UNDO],
			self.actions[actions.REDO],
			None,
			self.actions[actions.CUT]
		)
		ActionFactory.addActionsToMenu(ordered_actions, edit_menu)		
		self._createCopyMenu(edit_menu)
		ActionFactory.addActionsToMenu((self.actions[actions.PASTE], None), edit_menu)
		self._createSnippetsMenu(edit_menu)
	
	def _createCopyMenu(self, edit_menu):
		copy_menu = edit_menu.addMenu("Copy")		
		ordered_actions = (
			self.actions[actions.COPY],
			self.actions[actions.COPY_SOURCE],
			self.actions[actions.COPY_PREAMBLE],
			self.actions[actions.COPY_PREAMBLE_AND_SOURCE]
		)
		ActionFactory.addActionsToMenu(ordered_actions, copy_menu)
		self.actions[actions.COPY_MENU] = copy_menu
	
	def _createSnippetsMenu(self, edit_menu):
		self.actions[actions.SNIPPETS_MENU] = edit_menu.addMenu("Insert Snippets")
		self.loadSnippets()
	
	def loadSnippets(self):
		snippets_menu = self.actions[actions.SNIPPETS_MENU]
		snippets_menu.clear()
		snippets = Preferences.getSnippets()
		for snippet_name in sorted(snippets.iterkeys()):
			snippet_code = snippets[snippet_name]
			action = ActionFactory.createAction(self, snippet_name, "Insert \"%s\" Snippet" % snippet_name, None, self.insertSnippet)
			action.setData(QVariant(snippet_code))
			snippets_menu.addAction(action)
		
	@property
	def focused_document(self):
		"""
		Returns the document having the focus.
		"""
		if not self.documentHasFocus():
			raise Exception("There is no document currently focused")
		return QApplication.activeWindow().doc_controller

	def documentHasFocus(self):
		"""
		Returns whether a document currently has the focus.
		"""
		active_window = QApplication.activeWindow()
		return isinstance(active_window, DocumentView)
	
	def _doActionOnFocusedWidget(self, action):
		try:
			widget = QApplication.focusWidget()
			if hasattr(widget, action):
				method = getattr(widget, action)
				method()
			else:
				QApplication.beep()
		except Exception, e:
			Dialogs.showError(e)

	@pyqtSlot()
	def about(self):
		try:
			self.about_controller.showAbout()
		except Exception, e:
			Dialogs.showError(e)
		
	@pyqtSlot()
	def close(self):
		try:
			active_window = QApplication.activeWindow()
			if active_window is not None:
				active_window.close()
		except Exception, e:
			Dialogs.showError(e)
	
	@pyqtSlot()
	def copy(self):
		self._doActionOnFocusedWidget("copy")
	
	@pyqtSlot()
	def copySource(self):
		try:
			if self.documentHasFocus():
				addToClipboard(self.focused_document.model.source)
			else:
				QApplication.beep()
		except Exception, e:
			Dialogs.showError(e)
			
	@pyqtSlot()
	def copyPreamble(self):
		try:
			if self.documentHasFocus():
				addToClipboard(self.focused_document.model.preamble)
			else:
				QApplication.beep()
		except Exception, e:
			Dialogs.showError(e)
	
	@pyqtSlot()
	def copyPreambleAndSource(self):
		try:
			if self.documentHasFocus():
				addToClipboard("%s\n\n%s" % (self.focused_document.model.preamble, self.focused_document.model.source))
			else:
				QApplication.beep()
		except Exception, e:
			Dialogs.showError(e)
		
	@pyqtSlot()
	def cut(self):
		self._doActionOnFocusedWidget("cut")
		
	@pyqtSlot()
	def new(self):
		try:
			self.documents_controller.openEmptyDocument()
		except Exception, e:
			Dialogs.showError(e)
			
	@pyqtSlot()
	def open(self, file_path=None):
		try:
			if file_path is None:
				file_path = File.showOpenFileDialog()
			if file_path != "":
				self.documents_controller.openDocument(file_path)
		except Exception, e:
			Dialogs.showError(e)

	@pyqtSlot()
	def paste(self):
		self._doActionOnFocusedWidget("paste")

	@pyqtSlot()
	def showPreferences(self):
		try:
			self.preferences_controller.showPreferences()
		except Exception, e:
			Dialogs.showError(e)
		
	@pyqtSlot()
	def preview(self):
		try:
			if self.documentHasFocus():
				self.focused_document.preview()
			else:
				QApplication.beep()
		except Exception, e:
			Dialogs.showError(e)
	
	@pyqtSlot()
	def redo(self):
		self._doActionOnFocusedWidget("redo")
		
	@pyqtSlot()
	def quit(self):
		try:
			self.documents_controller.closeAllDocuments()
			TemporaryDirectory.delete()
			QApplication.quit()
		except Exception, e:
			Dialogs.showError(e)

	@pyqtSlot()
	def save(self):
		try:
			if self.documentHasFocus():
				self.focused_document.save()
			else:
				QApplication.beep()
		except Exception, e:
			Dialogs.showError(e)
		
	@pyqtSlot()
	def saveAll(self):
		try:
			self.documents_controller.saveAllDocuments()
		except Exception, e:
			Dialogs.showError(e)
		
	@pyqtSlot()
	def saveAs(self):
		try:
			if self.documentHasFocus():
				self.focused_document.saveAs()
			else:
				QApplication.beep()
		except Exception, e:
			Dialogs.showError(e)
	
	@pyqtSlot()
	def undo(self):
		self._doActionOnFocusedWidget("undo")
	
	@pyqtSlot()
	def insertSnippet(self):
		try:
			action = self.sender()
			snippet = unicode(action.data().toString())
			editor = QApplication.focusWidget()
			if isinstance(editor, EditorView):
				editor.insertSnippet(snippet)
			else:
				QApplication.beep()
		except Exception, e:
			Dialogs.showError(e)