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

from models import Preferences
from tools import isMacintoshComputer
from tools.qt import Dialogs, ActionFactory

class DocumentView(QMainWindow):
	"""
	TikZ document window. This class is just the root of the document views hierarchy.
	"""
	sourceChangedSignal = pyqtSignal(str)
	preambleChangedSignal = pyqtSignal(str)
	
	def __init__(self, parent=None):
		super(DocumentView, self).__init__(parent)
		self.app_controller = None
		self.doc_controller = None
		self.content_view = None
		self.feedback_view = None
		self.preview_view = None
		self.editor_splitter = None
		self.main_splitter = None
		
	def initView(self):
		if not isMacintoshComputer():
			self.setMenuBar(self.app_controller.menu_bar)
		self._initSubViews()
		self._restoreWindowState()
		self._initSignalsConnections()
		self.content_view.current_editor_view.setFocus()

	def _initSubViews(self):			
		self.editor_splitter = QSplitter(self)
		self.editor_splitter.setOrientation(Qt.Vertical)
		self.editor_splitter.addWidget(self.content_view)
		self.editor_splitter.addWidget(self.feedback_view)
		self.editor_splitter.setStretchFactor(0, 2)
		self.editor_splitter.setStretchFactor(1, 1)
		if Preferences.hasEditorSplitterState():
			self.editor_splitter.restoreState(Preferences.getEditorSplitterState())

		self.main_splitter = QSplitter(self)
		self.main_splitter.setOrientation(Qt.Horizontal)
		self.main_splitter.addWidget(self.editor_splitter)
		self.main_splitter.addWidget(self.preview_view)
		if Preferences.hasMainSplitterState():
			self.main_splitter.restoreState(Preferences.getMainSplitterState())
		else:
			self.main_splitter.setSizes([self.width() / 2] * 2)
		
		self.setCentralWidget(self.main_splitter)

	def _restoreWindowState(self):
		if Preferences.hasWindowGeometry():
			self.restoreGeometry(Preferences.getWindowGeometry())
		else:
			self.setWindowState(Qt.WindowMaximized)

	def _initSignalsConnections(self):
		self.content_view.source_editor_view.contentChangedSignal.connect(self.sourceEditorContentChanged)
		self.content_view.preamble_editor_view.contentChangedSignal.connect(self.preambleEditorContentChanged)

	def _saveWindowState(self):
		Preferences.setWindowGeometry(self.saveGeometry())
		Preferences.setEditorSplitterState(self.editor_splitter.saveState())
		Preferences.setMainSplitterState(self.main_splitter.saveState())

	@property
	def title(self):
		return self.getWindowTitle()
		
	@title.setter
	def title(self, title):
		# set the title of the window with "dirty" placeholder
		self.setWindowTitle("%s[*]" % title)
	
	@pyqtSlot(str)
	def setTitle(self, title):
		self.title = title

	@property
	def source(self):
		return self.content_view.source_editor_view.content
		
	@source.setter
	def source(self, source):
		source = unicode(source)
		if self.source != source:
			self.content_view.source_editor_view.content = source
			self.sourceChangedSignal.emit(source)

	
	@pyqtSlot(str)
	def setSource(self, source):
		self.source = source

	@property
	def preamble(self):
		return self.content_view.preamble_editor_view.content
		
	@preamble.setter
	def preamble(self, preamble):
		preamble = unicode(preamble)
		if self.preamble != preamble:
			self.content_view.preamble_editor_view.content = preamble
			self.preambleChangedSignal.emit(preamble)
	
	@pyqtSlot(str)
	def setPreamble(self, preamble):
		self.preamble = preamble

	@pyqtSlot()
	def sourceEditorContentChanged(self):
		self.sourceChangedSignal.emit(self.source)

	@pyqtSlot()
	def preambleEditorContentChanged(self):
		self.preambleChangedSignal.emit(self.preamble)
	
	def closeEvent(self, event=None):
		if self.doc_controller.model.isDirty():
			response = self._userWantToSave()
			if response == Dialogs.SAVE:
				self.doc_controller.save()
			elif event is not None and response == Dialogs.CANCEL:
				event.ignore()
				
		self._saveWindowState()
	
	def _userWantToSave(self):
		return Dialogs.closeDialog("The document has been modified", "Do you want to save your changes in %s?" % self.doc_controller.model.title, self)

	@pyqtSlot()
	def documentDirtied(self):
		self.setWindowModified(True)
		
	@pyqtSlot()
	def documentSaved(self):
		self.setWindowModified(False)
	