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

from tools.qt import Dialogs
from models import Preferences
import views.factory

class EditorPreferencesView(QWidget):
	"""
	The editor preferences view displays the user preferences for the TikZ editor views.
	"""
	
	editorFontChangedSignal = pyqtSignal(object)
	fileEncodingChangedSignal = pyqtSignal(int)
	lineEndingsChangedSignal = pyqtSignal(int)
	indentationTypeChangedSignal = pyqtSignal(int)
	indentationSizeChangedSignal = pyqtSignal(int)
	autoWrapChangedSignal = pyqtSignal(bool)
	errorMarkersChangedSignal = pyqtSignal(bool)
	errorAnnotationsChangedSignal = pyqtSignal(bool)
	
	def __init__(self, parent=None):
		super(EditorPreferencesView, self).__init__(parent)
		self.app_controller = None
		
		self.font = None
		self.font_label = QLabel("Editor Font:")
		self.font_choice = QLineEdit()
		self.font_select = QPushButton("Select")
				
		self.encoding_label = QLabel("File Encoding:")
		self.encoding_choice = QComboBox()
		
		self.line_endings_label = QLabel("Line Endings:")
		self.line_endings_choice = QComboBox()
		
		self.indent_type_label = QLabel("Indentation using:")
		self.indent_type_choice = QComboBox()
		
		self.indent_size_label = QLabel("Indentation Size:")
		self.indent_size_choice = QSpinBox()

		self.wrap_choice = QCheckBox("Auto-wrap lines")
		self.error_markers_choice = QCheckBox("Show error marker in margin of erroneous lines")
		self.error_annotations_choice = QCheckBox("Show error annotations beneath erroneous lines")
		
	def initView(self):
		self._initConnections()
		self._initWidgets()
		self._initLayout()

	def _initConnections(self):
		self.font_select.clicked.connect(self._selectFont)
		self.encoding_choice.activated.connect(self._encodingChanged)
		self.line_endings_choice.activated.connect(self._lineEndingsChanged)
		self.indent_type_choice.activated.connect(self._indentationTypeChanged)
		self.indent_size_choice.valueChanged.connect(self._indentationSizeChanged)
		self.wrap_choice.stateChanged.connect(self._autoWrapChanged)
		self.error_markers_choice.stateChanged.connect(self._errorMarkersChanged)
		self.error_annotations_choice.stateChanged.connect(self._errorAnnotationsChanged)
		
	def _initWidgets(self):
		self.font_choice.setReadOnly(True)
		self.font_choice.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

		self.encoding_choice.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.encoding_choice.addItem("UTF-8 (recommended)", Preferences.ENCODING_UTF8)
		self.encoding_choice.addItem("ISO-8859-1 (Latin 1)", Preferences.ENCODING_LATIN1)
		
		self.line_endings_choice.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.line_endings_choice.addItem("LF (UNIX)", Preferences.LINE_ENDINGS_UNIX)
		self.line_endings_choice.addItem("CR (Mac OS Classic)", Preferences.LINE_ENDINGS_MAC)
		self.line_endings_choice.addItem("CRLF (Windows)", Preferences.LINE_ENDINGS_WINDOWS)
		
		self.indent_type_choice.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.indent_type_choice.addItem("Tabs", Preferences.INDENT_TAB)
		self.indent_type_choice.addItem("Spaces", Preferences.INDENT_SPACES)
		
		# self.indent_size_choice.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.indent_size_choice.setMinimum(1)
			
	def _initLayout(self):
		layout = QFormLayout()
		layout.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)
		layout.setContentsMargins(50, 12, 50, 20)
		sublayout = QHBoxLayout()
		sublayout.addWidget(self.font_choice)
		sublayout.addWidget(self.font_select)
		layout.addRow(self.font_label, sublayout)
		layout.addRow(views.factory.ViewFactory.createLineSeparator())
		layout.addRow(self.encoding_label, self.encoding_choice)
		layout.addRow(self.line_endings_label, self.line_endings_choice)
		layout.addRow(views.factory.ViewFactory.createLineSeparator())
		layout.addRow(self.indent_type_label, self.indent_type_choice)
		layout.addRow(self.indent_size_label, self.indent_size_choice)
		layout.addRow(views.factory.ViewFactory.createLineSeparator())
		layout.addRow(self.wrap_choice)
		layout.addRow(self.error_markers_choice)
		layout.addRow(self.error_annotations_choice)

		self.setLayout(layout)
	
	def _selectFont(self):
		selected_font = Dialogs.selectFont(self.font)
		if selected_font is not None:
			self.editor_font = selected_font
			self.editorFontChangedSignal.emit(selected_font)
		
	def _encodingChanged(self, index):
		self.fileEncodingChangedSignal.emit(self.encoding_choice.itemData(index).toInt()[0])
	
	def _lineEndingsChanged(self, index):
		self.lineEndingsChangedSignal.emit(self.line_endings_choice.itemData(index).toInt()[0])
	
	def _indentationTypeChanged(self, index):
		self.indentationTypeChangedSignal.emit(self.indent_type_choice.itemData(index).toInt()[0])
		
	def _indentationSizeChanged(self, value):
		self.indentationSizeChangedSignal.emit(value)
		
	def _autoWrapChanged(self, state):
		self.autoWrapChangedSignal.emit(state)

	def _errorMarkersChanged(self, state):
		self.errorMarkersChangedSignal.emit(state)

	def _errorAnnotationsChanged(self, state):
		self.errorAnnotationsChangedSignal.emit(state)
	
	@property
	def editor_font(self):
		return self.font
	
	@editor_font.setter
	def editor_font(self, value):
		self.font = value
		if value is not None:
			self.font_choice.setText("%s, %d pt." % (self.font.family(), self.font.pointSize()))
		else:
			self.font_choice.setText("")
	
	@property
	def file_encoding(self):
		return self.encoding_choice.itemData(self.encoding_choice.currentIndex())
	
	@file_encoding.setter
	def file_encoding(self, value):
		self.encoding_choice.setCurrentIndex(self.encoding_choice.findData(value))
	
	@property
	def line_endings(self):
		return self.line_endings_choice.itemData(self.line_endings_choice.currentIndex())
	
	@line_endings.setter
	def line_endings(self, value):
		self.line_endings_choice.setCurrentIndex(self.line_endings_choice.findData(value))
	
	@property
	def indentation_type(self):
		return self.indent_type_choice.itemData(self.indent_type_choice.currentIndex())
	
	@indentation_type.setter
	def indentation_type(self, value):
		self.indent_type_choice.setCurrentIndex(self.indent_type_choice.findData(value))
	
	@property
	def indentation_size(self):
		return self.indent_size_choice.value()
	
	@indentation_size.setter
	def indentation_size(self, value):
		self.indent_size_choice.setValue(value)
		
	@property
	def auto_wrap(self):
		return self.wrap_choice.isChecked()
	
	@auto_wrap.setter
	def auto_wrap(self, value):
		self.wrap_choice.setChecked(value)
			
	@property
	def error_markers(self):
		return self.error_markers_choice.isChecked()
	
	@error_markers.setter
	def error_markers(self, value):
		self.error_markers_choice.setChecked(value)
			
	@property
	def error_annotations(self):
		return self.error_annotations_choice.isChecked()
	
	@error_annotations.setter
	def error_annotations(self, value):
		self.error_annotations_choice.setChecked(value)