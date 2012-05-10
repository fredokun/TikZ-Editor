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

import globals.defaults as defaults
from tools import isMacintoshComputer, isWindowsComputer, findCommandLocation

class PreferencesModel(object):
	"""
	The preferences model is a wrapper for QT's QSettings allowing easy retrieval of user
	defaults.
	"""
	
	WINDOW_GEOMETRY = "WindowGeometry"
	EDITOR_SPLITTER_STATE = "EditorSplitterState"
	MAIN_SPLITTER_STATE = "MainSplitterState"
	SELECTED_FEEDBACK_VIEW = "SelectedFeedbackView"
	LATEX_FILE_TEMPLATE = "LatexFileTemplate"
	PREAMBLE_TEMPLATE = "PreambleTemplate"
	PREVIEW_TEMPLATE = "PreviewTemplate"
	LATEX_TO_PDF_COMMAND = "LatexToPDFCommand"
	PDF_TO_IMAGE_COMMAND = "PDFToImageCommand"
	EDITOR_FONT = "EditorFont"
	FILE_ENCODING = "FileEncoding"
	LINE_ENDINGS = "LineEndings"
	INDENTATION_TYPE = "IndentationType"
	INDENTATION_SIZE = "IndentationSize"
	AUTO_WRAP = "AutoWrap"
	SHOW_ERROR_MARKERS = "ShowErrorMarkers"
	SHOW_ERROR_ANNOTATIONS = "ShowErrorAnnotations"
	SNIPPETS = "Snippets"
	
	FEEDBACK_LOGS_VIEW = 0
	FEEDBACK_ERRORS_VIEW = 1	
	ENCODING_UTF8 = 1
	ENCODING_LATIN1 = 2
	LINE_ENDINGS_WINDOWS = 1
	LINE_ENDINGS_MAC = 2
	LINE_ENDINGS_UNIX = 3
	INDENT_TAB = 1
	INDENT_SPACES = 2
	
	@staticmethod
	def containsKey(key):
		settings = QSettings()
		return settings.contains(key)
	
	@staticmethod
	def getValue(key):
		return PreferencesModel.getValueOrDefault(key, None)

	@staticmethod
	def getValueOrDefault(key, default_value):
		settings = QSettings()
		if default_value is not None:
			value = settings.value(key, QVariant(default_value))
		else:
			value = settings.value(key)
		return value

	@staticmethod
	def setValue(key, value):
		settings = QSettings()
		settings.setValue(key, QVariant(value))
	
	@staticmethod
	def removeKey(key):
		settings = QSettings()
		settings.remove(key)
		
################################################################################

	@staticmethod
	def hasWindowGeometry():
		return PreferencesModel.containsKey(PreferencesModel.WINDOW_GEOMETRY)
		
	@staticmethod
	def getWindowGeometry():
		return PreferencesModel.getValue(PreferencesModel.WINDOW_GEOMETRY).toByteArray()
	
	@staticmethod
	def setWindowGeometry(value):
		PreferencesModel.setValue(PreferencesModel.WINDOW_GEOMETRY, value)
	
	
	@staticmethod
	def hasEditorSplitterState():
		return PreferencesModel.containsKey(PreferencesModel.EDITOR_SPLITTER_STATE)
	
	@staticmethod
	def getEditorSplitterState():
		return PreferencesModel.getValue(PreferencesModel.EDITOR_SPLITTER_STATE).toByteArray()
	
	@staticmethod
	def setEditorSplitterState(value):
		PreferencesModel.setValue(PreferencesModel.EDITOR_SPLITTER_STATE, value)
		
	
	@staticmethod
	def hasMainSplitterState():
		return PreferencesModel.containsKey(PreferencesModel.MAIN_SPLITTER_STATE)
	
	@staticmethod
	def getMainSplitterState():
		return PreferencesModel.getValue(PreferencesModel.MAIN_SPLITTER_STATE).toByteArray()
	
	@staticmethod
	def setMainSplitterState(value):
		PreferencesModel.setValue(PreferencesModel.MAIN_SPLITTER_STATE, value)
	
	
	@staticmethod
	def hasSelectedFeedbackView():
		return PreferencesModel.containsKey(PreferencesModel.SELECTED_FEEDBACK_VIEW)
	
	@staticmethod
	def getSelectedFeedbackView():
		value = PreferencesModel.getValueOrDefault(PreferencesModel.SELECTED_FEEDBACK_VIEW, PreferencesModel.defaultSelectedFeedbackView()).toInt()
		convert_success = value[1]
		value = value[0]
		if not (convert_success and value in (PreferencesModel.FEEDBACK_LOGS_VIEW, PreferencesModel.FEEDBACK_ERRORS_VIEW)):
			value = PreferencesModel.defaultSelectedFeedbackView()
		return value
	
	@staticmethod
	def setSelectedFeedbackView(value):
		PreferencesModel.setValue(PreferencesModel.SELECTED_FEEDBACK_VIEW, value)
	
	@staticmethod
	def defaultSelectedFeedbackView():
		return PreferencesModel.FEEDBACK_LOGS_VIEW
	
################################################################################

	@staticmethod
	def hasEditorFont():
		return PreferencesModel.containsKey(PreferencesModel.EDITOR_FONT)
	
	@staticmethod
	def getEditorFont():
		font = QFont()
		font.fromString(PreferencesModel.getValueOrDefault(PreferencesModel.EDITOR_FONT, PreferencesModel.defaultEditorFont()).toString())
		return font
	
	@staticmethod
	def setEditorFont(value):
		PreferencesModel.setValue(PreferencesModel.EDITOR_FONT, value.toString())
	
	@staticmethod
	def defaultEditorFont():
		return defaults.EDITOR_FONT
		
		
	@staticmethod
	def hasFileEncoding():
		return PreferencesModel.containsKey(PreferencesModel.FILE_ENCODING)
	
	@staticmethod
	def getFileEncoding():
		value = PreferencesModel.getValueOrDefault(PreferencesModel.FILE_ENCODING, PreferencesModel.defaultFileEncoding()).toInt()
		convert_success = value[1]
		value = value[0]
		if not (convert_success and value in (PreferencesModel.ENCODING_LATIN1, PreferencesModel.ENCODING_UTF8)):
			value = PreferencesModel.defaultFileEncoding()
		return value

	
	@staticmethod
	def setFileEncoding(value):
		assert value in (PreferencesModel.ENCODING_LATIN1, PreferencesModel.ENCODING_UTF8)
		PreferencesModel.setValue(PreferencesModel.FILE_ENCODING, value)
	
	@staticmethod
	def defaultFileEncoding():
		default = PreferencesModel.ENCODING_UTF8
		if defaults.FILE_ENCODING == "LATIN-1":
			default = PreferencesModel.ENCODING_LATIN1
		return default
	
	
	@staticmethod
	def hasLineEndings():
		return PreferencesModel.containsKey(PreferencesModel.LINE_ENDINGS)
	
	@staticmethod
	def getLineEndings():
		value = PreferencesModel.getValueOrDefault(PreferencesModel.LINE_ENDINGS, PreferencesModel.defaultLineEndings()).toInt()
		convert_success = value[1]
		value = value[0]
		if not (convert_success and value in (PreferencesModel.LINE_ENDINGS_UNIX, PreferencesModel.LINE_ENDINGS_MAC, PreferencesModel.LINE_ENDINGS_WINDOWS)):
			value = PreferencesModel.defaultLineEndings()
		return value
	
	@staticmethod
	def setLineEndings(value):
		assert value in (PreferencesModel.LINE_ENDINGS_UNIX, PreferencesModel.LINE_ENDINGS_MAC, PreferencesModel.LINE_ENDINGS_WINDOWS)
		PreferencesModel.setValue(PreferencesModel.LINE_ENDINGS, value)
	
	@staticmethod
	def defaultLineEndings():
		default = PreferencesModel.LINE_ENDINGS_UNIX
		if isWindowsComputer():
			default = PreferencesModel.LINE_ENDINGS_WINDOWS
		return default
	
	
	@staticmethod
	def hasIndentationType():
		return PreferencesModel.containsKey(PreferencesModel.INDENTATION_TYPE)
	
	@staticmethod
	def getIndentationType():
		value = PreferencesModel.getValueOrDefault(PreferencesModel.INDENTATION_TYPE, PreferencesModel.defaultIndentationType()).toInt()
		convert_success = value[1]
		value = value[0]
		if not (convert_success and value in (PreferencesModel.INDENT_TAB, PreferencesModel.INDENT_SPACES)):
			value = PreferencesModel.defaultIndentationType()
		return value
	
	@staticmethod
	def setIndentationType(value):
		assert value in (PreferencesModel.INDENT_SPACES, PreferencesModel.INDENT_TAB)
		PreferencesModel.setValue(PreferencesModel.INDENTATION_TYPE, value)
	
	@staticmethod
	def defaultIndentationType():
		default = PreferencesModel.INDENT_TAB
		if defaults.INDENTATION_TYPE == "spaces":
			default = PreferencesModel.INDENT_SPACES
		return default


	@staticmethod
	def hasIndentationSize():
		return PreferencesModel.containsKey(PreferencesModel.INDENTATION_SIZE)
	
	@staticmethod
	def getIndentationSize():
		value = PreferencesModel.getValueOrDefault(PreferencesModel.INDENTATION_SIZE, PreferencesModel.defaultIndentationSize()).toInt()
		convert_success = value[1]
		value = value[0]
		if not (convert_success and value > 0):
			value = PreferencesModel.defaultIndentationSize()
		return value
	
	@staticmethod
	def setIndentationSize(value):
		assert value > 0
		PreferencesModel.setValue(PreferencesModel.INDENTATION_SIZE, value)
	
	@staticmethod
	def defaultIndentationSize():
		return defaults.INDENTATION_SIZE
		
	
	@staticmethod
	def hasAutoWrap():
		return PreferencesModel.containsKey(PreferencesModel.AUTO_WRAP)
	
	@staticmethod
	def getAutoWrap():
		return PreferencesModel.getValueOrDefault(PreferencesModel.AUTO_WRAP, PreferencesModel.defaultAutoWrap()).toBool()
	
	@staticmethod
	def setAutoWrap(value):
		PreferencesModel.setValue(PreferencesModel.AUTO_WRAP, value)
	
	@staticmethod
	def defaultAutoWrap():
		return defaults.AUTO_WRAP
	
	
	@staticmethod
	def hasShowErrorMarkers():
		return PreferencesModel.containsKey(PreferencesModel.SHOW_ERROR_MARKERS)
	
	@staticmethod
	def getShowErrorMarkers():
		return PreferencesModel.getValueOrDefault(PreferencesModel.SHOW_ERROR_MARKERS, PreferencesModel.defaultShowErrorMarkers()).toBool()
	
	@staticmethod
	def setShowErrorMarkers(value):
		PreferencesModel.setValue(PreferencesModel.SHOW_ERROR_MARKERS, value)
	
	@staticmethod
	def defaultShowErrorMarkers():
		return defaults.SHOW_ERROR_MARKERS
		
	
	@staticmethod
	def hasShowErrorAnnotations():
		return PreferencesModel.containsKey(PreferencesModel.SHOW_ERROR_ANNOTATIONS)
	
	@staticmethod
	def getShowErrorAnnotations():
		return PreferencesModel.getValueOrDefault(PreferencesModel.SHOW_ERROR_ANNOTATIONS, PreferencesModel.defaultShowErrorAnnotations()).toBool()
	
	@staticmethod
	def setShowErrorAnnotations(value):
		PreferencesModel.setValue(PreferencesModel.SHOW_ERROR_ANNOTATIONS, value)
	
	@staticmethod
	def defaultShowErrorAnnotations():
		return defaults.SHOW_ERROR_MARKERS
		
################################################################################

	@staticmethod
	def hasLatexFileTemplate():
		return PreferencesModel.containsKey(PreferencesModel.LATEX_FILE_TEMPLATE)
	
	@staticmethod
	def getLatexFileTemplate():
		return unicode(PreferencesModel.getValueOrDefault(PreferencesModel.LATEX_FILE_TEMPLATE, PreferencesModel.defaultLatexFileTemplate()).toString())
	
	@staticmethod
	def setLatexFileTemplate(value):
		PreferencesModel.setValue(PreferencesModel.LATEX_FILE_TEMPLATE, value)
	
	@staticmethod
	def defaultLatexFileTemplate():
		return defaults.DEFAULT_TEMPLATE
	

	@staticmethod
	def hasPreambleTemplate():
		return PreferencesModel.containsKey(PreferencesModel.PREAMBLE_TEMPLATE)
	
	@staticmethod
	def getPreambleTemplate():
		return unicode(PreferencesModel.getValueOrDefault(PreferencesModel.PREAMBLE_TEMPLATE, PreferencesModel.defaultPreambleTemplate()).toString())
	
	@staticmethod
	def setPreambleTemplate(value):
		PreferencesModel.setValue(PreferencesModel.PREAMBLE_TEMPLATE, value)
	
	@staticmethod
	def defaultPreambleTemplate():
		return defaults.DEFAULT_PREAMBLE_TEMPLATE
				

################################################################################

	@staticmethod
	def hasPreviewTemplate():
		return PreferencesModel.containsKey(PreferencesModel.PREVIEW_TEMPLATE)
	
	@staticmethod
	def getPreviewTemplate():
		return unicode(PreferencesModel.getValueOrDefault(PreferencesModel.PREVIEW_TEMPLATE, PreferencesModel.defaultPreviewTemplate()).toString())
	
	@staticmethod
	def setPreviewTemplate(value):
		PreferencesModel.setValue(PreferencesModel.PREVIEW_TEMPLATE, value)
	
	@staticmethod
	def defaultPreviewTemplate():
		return defaults.DEFAULT_TEMPLATE

	
	
	DEFAULT_LATEX_TO_PDF_COMMAND = None
	
	@staticmethod
	def hasLatexToPDFCommand():
		return PreferencesModel.containsKey(PreferencesModel.LATEX_TO_PDF_COMMAND)
	
	@staticmethod
	def getLatexToPDFCommand():
		return unicode(PreferencesModel.getValueOrDefault(PreferencesModel.LATEX_TO_PDF_COMMAND, PreferencesModel.defaultLatexToPDFCommand()).toString())
	
	@staticmethod
	def setLatexToPDFCommand(value):
		PreferencesModel.setValue(PreferencesModel.LATEX_TO_PDF_COMMAND, value)
	
	@staticmethod
	def defaultLatexToPDFCommand():
		if PreferencesModel.DEFAULT_LATEX_TO_PDF_COMMAND is None:
			pdflatex_path = findCommandLocation(defaults.DEFAULT_LATEX_TO_PDF_COMMAND)
		 	PreferencesModel.DEFAULT_LATEX_TO_PDF_COMMAND = defaults.DEFAULT_LATEX_TO_PDF_ARGS % pdflatex_path
		return PreferencesModel.DEFAULT_LATEX_TO_PDF_COMMAND
				
	
	DEFAULT_PDF_TO_IMAGE_COMMAND = None
	
	@staticmethod
	def hasPDFToImageCommand():
		return PreferencesModel.containsKey(PreferencesModel.PDF_TO_IMAGE_COMMAND)
	
	@staticmethod
	def getPDFToImageCommand():
		return unicode(PreferencesModel.getValueOrDefault(PreferencesModel.PDF_TO_IMAGE_COMMAND, PreferencesModel.defaultPDFToImageCommand()).toString())

	@staticmethod
	def setPDFToImageCommand(value):
		PreferencesModel.setValue(PreferencesModel.PDF_TO_IMAGE_COMMAND, value)
	
	@staticmethod
	def defaultPDFToImageCommand():
		if PreferencesModel.DEFAULT_PDF_TO_IMAGE_COMMAND is None:
			if isMacintoshComputer():
				sips_path = findCommandLocation(defaults.DEFAULT_MAC_PDF_TO_IMAGE_COMMAND)
			 	PreferencesModel.DEFAULT_PDF_TO_IMAGE_COMMAND = defaults.DEFAULT_MAC_PDF_TO_IMAGE_ARGS % sips_path
			else:
				convert_path = findCommandLocation(defaults.DEFAULT_PDF_TO_IMAGE_COMMAND)
				PreferencesModel.DEFAULT_PDF_TO_IMAGE_COMMAND = defaults.DEFAULT_PDF_TO_IMAGE_ARGS % convert_path
		return PreferencesModel.DEFAULT_PDF_TO_IMAGE_COMMAND

################################################################################

	@staticmethod
	def hasSnippets():
		return PreferencesModel.containsKey(PreferencesModel.SNIPPETS)
	
	@staticmethod
	def getSnippets():
		snippets = PreferencesModel.getValueOrDefault(PreferencesModel.SNIPPETS, PreferencesModel.defaultSnippets()).toPyObject()
		# convert QString to python strings
		str_snippets = {}
		for name, code in snippets.items():
			str_snippets[unicode(name)] = unicode(code)
		return str_snippets
		
	@staticmethod
	def setSnippets(value):
		PreferencesModel.setValue(PreferencesModel.SNIPPETS, value)
	
	@staticmethod
	def defaultSnippets():
		return defaults.SNIPPETS
