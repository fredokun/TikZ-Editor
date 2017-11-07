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

import tikz_editor.models.preferences

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class FileError(Exception):
	pass


class File(object):
	"""
	The file tool is a wrapper to QT's file IO functions.
	"""

	LAST_OPENED_PATH = os.getenv("HOME")

	@staticmethod
	def getFileNameFromFilePath(file_path):
		file_info = QFileInfo(file_path)
		return file_info.fileName()

	@staticmethod
	def getDirectoryFromFilePath(file_path):
		file_info = QFileInfo(file_path)
		return file_info.path()

	@staticmethod
	def showOpenFileDialog(default_directory=None):
		if default_directory is None:
			default_directory = File.LAST_OPENED_PATH
		file_path, _ = QFileDialog.getOpenFileName(None, "Open File", default_directory)
		if file_path:
			File.LAST_OPENED_PATH = File.getDirectoryFromFilePath(file_path)
		return file_path

	@staticmethod
	def showSaveFileDialog(parent=None, file_name=None):
		file_path, _ = QFileDialog.getSaveFileName(parent, "Save File As", file_name)
		return file_path

	@staticmethod
	def readContentFromFilePath(file_path):
		f = File(file_path)
		return f.readContent()

	@staticmethod
	def writeContentToFilePath(content, file_path):
		f = File(file_path)
		f.writeContent(content)

	@staticmethod
	def exists(file_path):
		return QFile.exists(file_path)

	def __init__(self, file_path):
		assert file_path is not None
		self._file_path = file_path
		self._file_descriptor = None

		encoding = tikz_editor.models.preferences.PreferencesModel.getFileEncoding()
		if encoding == tikz_editor.models.preferences.PreferencesModel.ENCODING_LATIN1:
			self._codec = "ISO 8859-1"
		else:
			self._codec = "UTF-8"

	def readContent(self):
		self._openFileForReading()
		content = self._readContentFromFileDescriptor()
		self._closeFile()
		return content

	def writeContent(self, content):
		self._openFileForWriting()
		self._writeContentOnFileDescriptor(content)
		self._closeFile()

	def _openFileForReading(self):
		self._openFile(QIODevice.ReadOnly)

	def _openFileForWriting(self):
		self._openFile(QIODevice.WriteOnly)

	def _openFile(self, open_mode):
		self._file_descriptor = QFile(self._file_path)
		if not self._file_descriptor.open(open_mode):
			raise FileError(str(self._file_descriptor.errorString()))

	def _closeFile(self):
		if self._file_descriptor is not None:
			self._file_descriptor.close()

	def _readContentFromFileDescriptor(self):
		stream = self._getStreamFromFileDescriptor()
		return stream.readAll()

	def _writeContentOnFileDescriptor(self, content):
		stream = self._getStreamFromFileDescriptor()
		stream << content

	def _getStreamFromFileDescriptor(self):
		stream = QTextStream(self._file_descriptor)
		stream.setCodec(self._codec)
		return stream
