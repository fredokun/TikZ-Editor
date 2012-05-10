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

import controllers.factory
from app import AppController

class DocumentsController(object):
	"""
	This is the documents manager. It keeps a list of all opened documents and can open
	new or existing documents.
	"""
	
	def __init__(self):
		super(DocumentsController, self).__init__()
		self.app_controller = None
		self.documents = []
	
	def openEmptyDocument(self):
		doc = self._createDocument()
		doc.view.content_view.source_editor_view.goToLine(2)
		doc.showView()
		
	def openDocument(self, file_path):
		"""
		Opens an existing document at given file path and closes the startup document if
		it is empty.
		"""
		assert file_path is not None
		doc = self._createDocument(file_path)
		doc.showView()
		self._closeEmptyStartupDocument()
			
	def _createDocument(self, file_path=None):
		"""
		Creates a document controller and adds it to the docs list.
		"""
		doc = controllers.factory.ControllerFactory.createDocumentController(self.app_controller, file_path)
		doc.documentClosedSignal.connect(self._documentClosed)
		self.documents.append(doc)
		return doc
	
	def _closeEmptyStartupDocument(self):
		"""
		Closes the startup document if it is empty.
		"""
		if len(self.documents) > 1 and self.documents[0].model.isUntitled() and self.documents[0].model.isEmpty():
			self.documents[0].view.close()
	
	def saveAllDocuments(self):
		for d in self.documents:
			if d.isDirty():
				d.save()
	
	def closeAllDocuments(self):
		for d in self.documents:
			d.close()
	
	@pyqtSlot()
	def _documentClosed(self, document):
		"""
		Removes a closed document from the documents list. Called by the document
		controller after the user closed the view.
		"""
		if document in self.documents:
			self.documents.remove(document)