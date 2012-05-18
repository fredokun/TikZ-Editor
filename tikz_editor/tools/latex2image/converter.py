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
from string import Template
from uuid import uuid4

from PyQt4.QtCore import *

from tikz_editor.models import Preferences
from tikz_editor.tools import File
from logs_parser import LogsParser


class LatexToImageConversion(object):
	"""
	Class embedding the LaTeX to Image conversion data:
		image_path is the path to the image file generated from the LaTeX source
		logs is the pdflatex's logs with errors highlighted (HTML)
		errors is a list of tuples (line_number, error_message)
	"""
	def __init__(self, source, image_path, logs, errors):
		super(LatexToImageConversion, self).__init__()
		self.source = source
		self.image_path = image_path
		self.logs = logs
		self.errors = errors


class Converter(QObject):
	"""
	Converts LaTeX source to image file
	"""

	convertedSignal = pyqtSignal(LatexToImageConversion)
	conversionAbortedSignal = pyqtSignal()

	def __init__(self, output_directory):
		super(Converter, self).__init__()
		assert output_directory is not None
		self.output_directory = output_directory
		self.latex_source = ""
		self._latex_process = None
		self._convert_process = None
		self.logs_parser = LogsParser()
		self._stopping_conversion = False

		self.unique_random_file_name = unicode(uuid4())
		self.base_file_path = os.path.join(self.output_directory, self.unique_random_file_name)
		self.source_file_path = "%s.tex" % self.base_file_path
		self.pdf_file_path = "%s.pdf" % self.base_file_path
		self.png_file_path = "%s.png" % self.base_file_path

		self._initProcesses()

	def _initProcesses(self):
		self._latex_process = QProcess()
		self._latex_process.setWorkingDirectory(self.output_directory)
		self._latex_process.finished.connect(self._latexTypesettingFinished)
		self._latex_process.error.connect(self._latexTypesettingError)
		self._convert_process = QProcess()
		self._convert_process.setWorkingDirectory(self.output_directory)
		self._convert_process.error.connect(self._pdfToImageConversionError)
		self._convert_process.finished.connect(self._pdfToImageConversionFinished)

	def stopConversion(self):
		self._stopping_conversion = True
		self._killProcesses()
		self._stopping_conversion = False

	def isStoppingConversion(self):
		return self._stopping_conversion

	def _killProcesses(self):
		self._latex_process.kill()
		self._latex_process.waitForFinished()
		self._convert_process.kill()
		self._convert_process.waitForFinished()

	def convertLatexToImage(self, source):
		self.stopConversion()
		try:
			self.logs_parser.clearLogsAndErrors()
			self.latex_source = source
			self._writeSourceCodeToFile()
			self._startConversion()
		except Exception, e:
			self.logs_parser.addErrorMessage(unicode(e))
			self._parseErrorsFromLogs()
			self._emitConversionSignalWithImagePath(None)
			self.conversionAbortedSignal.emit()

	def _writeSourceCodeToFile(self):
		File.writeContentToFilePath(self.latex_source, self.source_file_path)

	def _startConversion(self):
		self._convertSourceFileToPDF()

	def _convertSourceFileToPDF(self):
		latex2pdf_command = Template(Preferences.getLatexToPDFCommand())
		latex2pdf_command = latex2pdf_command.safe_substitute(OUTPUT_DIR=self.output_directory, FILE_NAME=self.unique_random_file_name, FILE_PATH=self.source_file_path)
		self._latex_process.start(latex2pdf_command)

	def _latexTypesettingFinished(self, exit_code, exit_status):
		if not self.isStoppingConversion():
			self.logs_parser.logs = unicode(self._latex_process.readAllStandardOutput(), encoding="utf-8")
			if self.logs_parser.isTypesettingAborted():
				self._parseErrorsFromLogs()
				self._emitConversionSignalWithImagePath(None)
				self.conversionAbortedSignal.emit()
			else:
				self._convertPDFToImage()

	def _latexTypesettingError(self, error):
		self.logs_parser.addErrorMessage("Preview Error: Can't convert the source file to PDF. Please check the LaTeX command in preview's preferences.")
		self._emitConversionSignalWithImagePath(None)
		self.conversionAbortedSignal.emit()

	def _convertPDFToImage(self):
		pdf2image_command = Template(Preferences.getPDFToImageCommand())
		pdf2image_command = pdf2image_command.safe_substitute(PDF_PATH=self.pdf_file_path, IMAGE_PATH=self.png_file_path)
		self._convert_process.start(pdf2image_command)

	def _pdfToImageConversionFinished(self, exit_code, exit_status):
		if not self.isStoppingConversion():
			if exit_status != 0:
				self.logs_parser.addErrorMessage("PDF to image conversion failed!")

			self._parseErrorsFromLogs()
			self._emitConversionSignalWithImagePath(self.png_file_path)

	def _pdfToImageConversionError(self, error):
		self.logs_parser.addErrorMessage("Preview Error: Can't convert the PDF preview to image. Please check the PDF to image command in preview's preferences.")
		self._emitConversionSignalWithImagePath(None)
		self.conversionAbortedSignal.emit()

	def _parseErrorsFromLogs(self):
		self.logs_parser.parseErrorsFromLogs()

	def _emitConversionSignalWithImagePath(self, image_path):
		self.convertedSignal.emit(LatexToImageConversion(self.latex_source, image_path, self.logs_parser.getStyledLogs(), self.logs_parser.errors))
