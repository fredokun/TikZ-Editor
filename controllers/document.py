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

from tools import File
from tools.qt import Dialogs

class DocumentController(QObject):
	"""
	The document controller is processing user actions on a document.
	"""
	figurePreviewOutOfSyncSignal = pyqtSignal()
	figurePreviewChangedSignal = pyqtSignal(str, list)
	documentClosedSignal = pyqtSignal(object)
	
	def __init__(self):
		super(DocumentController, self).__init__()
		self.app_controller = None	
		self.errors_controller = None
		self.preview_controller = None
		self.model = None
		self.view = None
	
	def initController(self):
		assert self.model and self.view		
		self._connectViewAndModel()
		self._syncViewAndModel()
		if not self.model.isEmpty():
			self.preview_controller.updatePreview()
				
	def _connectViewAndModel(self):
		self.view.sourceChangedSignal.connect(self.model.setSource)
		self.view.preambleChangedSignal.connect(self.model.setPreamble)
		self.model.sourceChangedSignal.connect(self.view.setSource)
		self.model.preambleChangedSignal.connect(self.view.setPreamble)
		self.model.sourceChangedSignal.connect(self.preview_controller.documentContentChanged)
		self.model.preambleChangedSignal.connect(self.preview_controller.documentContentChanged)
		self.model.titleChangedSignal.connect(self.view.setTitle)
		self.model.documentDirtiedSignal.connect(self.view.documentDirtied)
		self.model.documentSavedSignal.connect(self.view.documentSaved)
		self.preview_controller.willUpdatePreviewSignal.connect(self.errors_controller.clearErrors)
		self.preview_controller.errorsInSourceSignal.connect(self.errors_controller.converterErrorsOccurred)
		self.preview_controller.logsSignal.connect(self.view.feedback_view.logs_view.setLogs)

	def _syncViewAndModel(self):
		self.view.preamble = self.model.preamble
		self.view.source = self.model.source
		self.view.title = self.model.title
	
	def showView(self):
		self.view.show()
		self.view.raise_()
		
	@pyqtSlot()
	def preview(self):
		self.preview_controller.updatePreview()
		
	@pyqtSlot()
	def close(self):
		self.preview_controller.abortPreview()
		self.view.closeEvent()
		self.documentClosedSignal.emit(self)

	@pyqtSlot()
	def save(self):
		if self.model.isUntitled():
			self.saveAs()
		else:
			self.model.save()

	@pyqtSlot()
	def saveAs(self):
		file_path = File.showSaveFileDialog(self.view, self._getDocumentFileName())
		if file_path:
			self.model.file_path = file_path
			self.model.save()
	
	def _getDocumentFileName(self):
		file_name = self.model.file_path
		if not file_name:
			file_name =  "%s.tex" % self.model.title
		return file_name