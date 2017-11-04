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

from tikz_editor.tools import File
from .tags import *


class DocumentReaderError(Exception):
	def __init__(self, message="Not a valid TikZ document"):
		super(DocumentReaderError, self).__init__(message)


class DocumentReader(object):
	"""
	The document reader tool extract the preamble and source of a TikZ file.
	"""

	def __init__(self, file_path):
		assert file_path is not None
		super(DocumentReader, self).__init__()
		self.file_path = file_path
		self.file_lines = []
		self.preamble_lines = []
		self.source_lines = []
		self.current_line = ""
		self.parsing_preamble = False
		self.parsing_source = False

	def readPreambleAndSource(self):
		self._checkFileExists()
		self._readFileLines()
		self._checkDocumentValidity()
		self._extractPreambleAndSource()
		self._checkParsingValidity()
		preamble = "\n".join(self.preamble_lines)
		source = "\n".join(self.source_lines)
		return (preamble, source)

	def _checkFileExists(self):
		if not File.exists(self.file_path):
			raise DocumentReaderError("The file does not exist")

	def _readFileLines(self):
		content = File.readContentFromFilePath(self.file_path)
		self.file_lines = content.split("\n")

	def _checkDocumentValidity(self):
		"""
		Checks if the document has a TikZ comment tag at the beginning. This allows to
		verify if the document was created by this TikZ editor and contains other comment
		tags for preamble and source.
		"""
		if self._isFileEmpty() or self.file_lines[0] != TIKZ_TAG:
			raise DocumentReaderError()

	def _isFileEmpty(self):
		return len(self.file_lines) == 0

	def _extractPreambleAndSource(self):
		"""
		Extracts the preamble and TikZ source from file content using delimiter tags.
		"""
		for self.current_line in self.file_lines:
			if self.parsing_preamble:
				self._parsePreamble()
			elif self.parsing_source:
				self._parseSource()
			elif self.current_line == PREAMBLE_BEGIN_TAG:
				self.parsing_preamble = True
			elif self.current_line == SOURCE_BEGIN_TAG:
				self.parsing_source = True

	def _parsePreamble(self):
		if self.current_line == PREAMBLE_END_TAG:
			self.parsing_preamble = False
		else:
			self.preamble_lines.append(self.current_line)

	def _parseSource(self):
		if self.current_line == SOURCE_END_TAG:
			self.parsing_source = False
		else:
			self.source_lines.append(self.current_line)

	def _checkParsingValidity(self):
		"""
		Checks if the document parsing is completed (all the begin tags are closed).
		"""
		if self.parsing_preamble or self.parsing_preamble:
			raise DocumentReaderError()
