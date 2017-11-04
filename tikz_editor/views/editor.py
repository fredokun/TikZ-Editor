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

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.Qsci import *

import tikz_editor.globals.editor as editor
from tikz_editor.models import Preferences


class LexerTikZ(QsciLexerTeX):
	"""
	Scintilla lexer used for syntax-highlighting TikZ sources.
	"""

	def __init__(self, parent=None):
		super(LexerTikZ, self).__init__(parent)

	def keywords(self, keyword_set):
		"""
		Returns the TikZ keywords
		"""
		keywords = super(LexerTikZ, self).keywords(keyword_set)
		if keyword_set == 1:
			keywords += ' ' + ' '.join(editor.TIKZ_KEYWORDS)
		return keywords

	def defaultColor(self, style):
		"""
		Returns the color for each style
		"""
		color = super(LexerTikZ, self).defaultColor(style)
		if style == LexerTikZ.Default:  # LaTeX comments (without leading %)
			color = QColor(editor.EDITOR_COMMENTS_COLOR)
		elif style == LexerTikZ.Special:  # Symbols ()[]<>=
			color = QColor(editor.EDITOR_SYMBOLS1_COLOR)
		elif style == LexerTikZ.Group:  # Symbols {}$
			color = QColor(editor.EDITOR_SYMBOLS2_COLOR)
		elif style == LexerTikZ.Symbol:  # Leading % of LaTeX comments
			color = QColor(editor.EDITOR_COMMENTS_COLOR)
		elif style == LexerTikZ.Command:  # LaTeX commands prefixed by \
			color = QColor(editor.EDITOR_KEYWORDS_COLOR)
		elif style == LexerTikZ.Text:  # Rest of the source
			color = QColor(editor.EDITOR_TEXT_COLOR)
		return color

	def defaultFont(self, style):
		"""
		Returns the font for each style
		"""
		font = super(LexerTikZ, self).defaultFont(style)
		if style == LexerTikZ.Default:  # LaTeX comments (without leading %)
			font.setBold(editor.EDITOR_COMMENTS_BOLD)
			font.setItalic(editor.EDITOR_COMMENTS_ITALIC)
		elif style == LexerTikZ.Special:  # Symbols ()[]<>
			font.setBold(editor.EDITOR_SYMBOLS1_BOLD)
			font.setItalic(editor.EDITOR_SYMBOLS1_ITALIC)
		elif style == LexerTikZ.Group:  # Symbols {}
			font.setBold(editor.EDITOR_SYMBOLS2_BOLD)
			font.setItalic(editor.EDITOR_SYMBOLS2_ITALIC)
		elif style == LexerTikZ.Symbol:  # Leading % of LaTeX comments
			font.setBold(editor.EDITOR_COMMENTS_BOLD)
			font.setItalic(editor.EDITOR_COMMENTS_ITALIC)
		elif style == LexerTikZ.Command:  # LaTeX commands prefixed by \
			font.setBold(editor.EDITOR_KEYWORDS_BOLD)
			font.setItalic(editor.EDITOR_KEYWORDS_ITALIC)
		elif style == LexerTikZ.Text:  # Rest of the source
			font.setBold(editor.EDITOR_TEXT_BOLD)
			font.setItalic(editor.EDITOR_TEXT_ITALIC)
		return font


class EditorView(QsciScintilla):
	"""
	View used for editing TikZ source code. This is a subclass of QScintilla's editor.
	"""

	ERROR_MARGIN_MARKER = 8
	SNIPPET_CURSOR_PLACEHOLDER = "@@@"

	contentChangedSignal = pyqtSignal()

	# list of instances used to reload user preferences in real-time
	instances = []

	@staticmethod
	def reloadUserPreferences():
		"""
		Reloads user preferences of all EditorView instances in real-time
		"""
		for editor in EditorView.instances:
			editor.loadUserPreferences()

	def __init__(self, parent=None):
		super(EditorView, self).__init__(parent)
		self.app_controller = None
		self.show_margin = True
		EditorView.instances.append(self)

	def initView(self, show_margin=True):
		self.show_margin = show_margin
		self._initEditor()
		self._initConnections()
		self.loadUserPreferences()

	def _initEditor(self):
		# margins
		self.setMarginSensitivity(1, True)

		# margin markers
		self.markerDefine(QsciScintilla.RightArrow, EditorView.ERROR_MARGIN_MARKER)
		self.setMarkerBackgroundColor(QColor("#ee1111"), EditorView.ERROR_MARGIN_MARKER)

		# options
		self.setAutoIndent(True)

		# annotations
		self.setAnnotationDisplay(self.AnnotationBoxed)

	# customize annotations style (not used because of a bug, only the first instance
	# of EditorView is styled)
	# self.SendScintilla(QsciScintilla.SCI_SETSTYLEBITS, 7)
	# QsciStyle(6, "annotations", QColor(31, 116, 224), QColor(31, 116, 224), font)

	def _initConnections(self):
		self.textChanged.connect(self.contentChangedSignal)

	def loadUserPreferences(self):
		# editor font
		font = Preferences.getEditorFont()
		self.setFont(font)
		lexer = LexerTikZ()
		lexer.setDefaultFont(font)
		self.setLexer(lexer)

		# margins
		if self.show_margin:
			self._setMarginFont(font)
		else:
			self._hideMargin()

		# auto-wrap
		auto_wrap = Preferences.getAutoWrap()
		self.setWrapMode(auto_wrap)
		if auto_wrap:
			# hide horizontal scrollbar
			self.SendScintilla(QsciScintilla.SCI_SETHSCROLLBAR, 0)
		else:
			# show horizontal scrollbar
			self.SendScintilla(QsciScintilla.SCI_SETHSCROLLBAR, 1)
			self.SendScintilla(QsciScintilla.SCI_SETSCROLLWIDTH, 1)
			self.SendScintilla(QsciScintilla.SCI_SETSCROLLWIDTHTRACKING, 1)

		# file encoding
		encoding = Preferences.getFileEncoding()
		self.setUtf8(encoding == Preferences.ENCODING_UTF8)

		# line endings
		line_endings = Preferences.getLineEndings()
		if line_endings == Preferences.LINE_ENDINGS_WINDOWS:
			self.setEolMode(EditorView.EolWindows)
		elif line_endings == Preferences.LINE_ENDINGS_MAC:
			self.setEolMode(EditorView.EolMac)
		else:
			self.setEolMode(EditorView.EolUnix)

		# indentation type
		indentation_type = Preferences.getIndentationType()
		self.setIndentationsUseTabs(indentation_type == Preferences.INDENT_TAB)

		# indentation size
		self.setTabWidth(Preferences.getIndentationSize())

	def _hideMargin(self):
		self.setMarginWidth(1, 0)

	def _setMarginFont(self, font):
		fontmetrics = QFontMetrics(font)
		self.setMarginsFont(font)
		# use margin 0 for line numbers
		self.setMarginWidth(0, fontmetrics.width("0000") + 6)
		self.setMarginLineNumbers(0, True)

	@property
	def content(self):
		return self.text()

	@content.setter
	def content(self, content):
		self.setText(content)

	def insertSnippet(self, snippet):
		"""
		Inserts a code snippet to current position.
		The cursor position is set to the placeholder SNIPPET_CURSOR_PLACEHOLDER (@@@).
		"""
		wanted_position = snippet.find(EditorView.SNIPPET_CURSOR_PLACEHOLDER)
		if wanted_position == -1:
			wanted_position = len(snippet)
			self.insert(snippet)
		else:
			(snippet_before_cursor, snippet_after_cursor) = snippet.split(EditorView.SNIPPET_CURSOR_PLACEHOLDER, 1)
			self.insert(snippet_after_cursor)
			self.insert(snippet_before_cursor)

		# offset the cursor to wanted position
		(current_line, current_position) = self.getCursorPosition()
		self.setCursorPosition(current_line, current_position + wanted_position)

	def getLastLine(self):
		"""
		Returns the number of the last line
		"""
		return self.lines()

	def lineSize(self, line):
		"""
		Returns the size (in characters) of a line
		"""
		size = 0
		if self._isValidLineNumber(line):
			line_index = self._convertLineNumberToLineIndex(line)
			size = len(self.text(line_index).rstrip())
		return size

	def selectLine(self, line):
		if self._isValidLineNumber(line):
			line_index = self._convertLineNumberToLineIndex(line)
			self.ensureLineVisible(line_index)
			self.setSelection(line_index, 0, line_index, self.lineSize(line))

	def goToLine(self, line):
		if self._isValidLineNumber(line):
			line_index = self._convertLineNumberToLineIndex(line)
			self.setCursorPosition(line_index, 0)

	def goToPosition(self, line, index):
		if self._isValidLineNumber(line):
			line_index = self._convertLineNumberToLineIndex(line)
			self.setCursorPosition(line_index, index)

	def _isValidLineNumber(self, line):
		"""
		Returns whether the given line is between the bound of the document
		"""
		return line > 0 and line <= self.lines()

	def _convertLineNumberToLineIndex(self, line):
		"""
		Converts a line number to line index to match QScintilla's methods
		"""
		assert line > 0
		return line - 1

	def removeAllErrorMarginMarkers(self):
		self.markerDeleteAll(EditorView.ERROR_MARGIN_MARKER)

	def addErrorMarginMarkerToLine(self, line):
		if self._isValidLineNumber(line):
			line_index = self._convertLineNumberToLineIndex(line)
			self.markerAdd(line_index, EditorView.ERROR_MARGIN_MARKER)

	def removeErrorMarginMarkerFromLine(self, line):
		if self._isValidLineNumber(line):
			line_index = self._convertLineNumberToLineIndex(line)
			self.markerDelete(line_index, EditorView.ERROR_MARGIN_MARKER)

	def removeAllAnnotations(self):
		self.clearAnnotations()

	def addAnnotationToLine(self, line, annotation):
		if self._isValidLineNumber(line):
			line_index = self._convertLineNumberToLineIndex(line)
			old_annotation = self.annotation(line_index)
			if old_annotation:
				annotation = "%s\n%s" % (old_annotation, annotation)
			self.annotate(line_index, annotation, 2)

	def getCharacterAtCurrentCursorPosition(self):
		char = ""
		(line_nb, col_nb) = self.getCursorPosition()
		line = self.text(line_nb)
		if col_nb < len(line):
			char = line[col_nb]
		return char
