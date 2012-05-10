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

from preferences import PreferencesModel as Preferences
from tools import File
from tools import documentIO

class DocumentError(Exception):
	pass
		
class DocumentModel(QObject):
	"""
	The document model represents a TikZ document, that is composed of a preamble and a
	source.
	"""
	
	LAST_CREATED_DOCUMENT_ID = 0
	DEFAULT_SOURCE = unicode("\\begin{tikzpicture}\n\n\\end{tikzpicture}")
	
	sourceChangedSignal = pyqtSignal(str)
	preambleChangedSignal = pyqtSignal(str)
	titleChangedSignal = pyqtSignal(str)
	documentDirtiedSignal = pyqtSignal()
	documentSavedSignal = pyqtSignal()
	
	def __init__(self, file_path=None):
		super(DocumentModel, self).__init__()
		self.id = self._createDocumentId()
		self._preamble = Preferences.getPreambleTemplate()
		self._source = DocumentModel.DEFAULT_SOURCE
		self._dirty = False
		self._file_path = file_path
	
	def _createDocumentId(self):
		DocumentModel.LAST_CREATED_DOCUMENT_ID += 1
		return DocumentModel.LAST_CREATED_DOCUMENT_ID
		
	def open(self):
		"""
		To open the document, we read the content from the file path and un-
		dirty the document.
		"""
		try:
			if File.exists(self.file_path):
				(self.preamble, self.source) = documentIO.readPreambleAndSourceFromFilePath(self.file_path)
			self.dirty = False
		except Exception, e:
			raise DocumentError("The document cannot be opened: %s" % unicode(e))
		
	def save(self):
		"""
		To save the document, we write the content to the file path and un-
		dirty the document.
		"""
		try:
			template = Preferences.getLatexFileTemplate()
			documentIO.writeDocumentToFilePath(template, self, self.file_path)
			self.dirty = False
		except Exception, e:
			raise DocumentError("The document cannot be saved: %s" % unicode(e))

	@property
	def file_path(self):
		return self._file_path
	
	@file_path.setter
	def file_path(self, file_path):
		if self._file_path != file_path:
			self._file_path = file_path
			self.titleChangedSignal.emit(self.title)
	
	@property
	def title(self):
		"""
		The title of a document is the file name of the document or
		"Untitled [ID]" if the document is untitled.
		"""
		if self.isUntitled():
			title = "Untitled %d" % self.id
		else:
			title = File.getFileNameFromFilePath(self.file_path)
		return title

	@property
	def dirty(self):
		return self._dirty

	@dirty.setter
	def dirty(self, dirty):
		if self._dirty != dirty:
			self._dirty = dirty
			if dirty:
				self.documentDirtiedSignal.emit()
			else:
				self.documentSavedSignal.emit()

	@property
	def source(self):
		return self._source

	@source.setter
	def source(self, source):
		source = unicode(source)
		if self._source != source:
			self._source = source
			self.sourceChangedSignal.emit(source)
			self.dirty = True
	
	@pyqtSlot(str)
	def setSource(self, source):
		self.source = source

	@property
	def preamble(self):
		return self._preamble

	@preamble.setter
	def preamble(self, preamble):
		preamble = unicode(preamble)
		if self._preamble != preamble:
			self._preamble = preamble
			self.preambleChangedSignal.emit(preamble)
			self.dirty = True
	
	@pyqtSlot(str)
	def setPreamble(self, preamble):
		self.preamble = preamble
		
	def isDirty(self):
		return self.dirty
		
	def isUntitled(self):
		# an untitled document has no file path.
		return self.file_path is None or self.file_path == ""

	def isEmpty(self):
		return (self.preamble == Preferences.getPreambleTemplate() and self.source == DocumentModel.DEFAULT_SOURCE)