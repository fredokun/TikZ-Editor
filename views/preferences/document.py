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
import views.editor
import views.factory

class DocumentPreferencesView(QWidget):
	"""
	The document preferences view displays the user defaults for the TikZ documents.
	"""
	
	latexFileTemplateChangedSignal = pyqtSignal(unicode)
	preambleTemplateChangedSignal = pyqtSignal(unicode)
	
	def __init__(self, parent=None):
		super(DocumentPreferencesView, self).__init__(parent)
		self.app_controller = None
		self.latex_file_label = QLabel("<b>LaTeX file template used for saving document:</b>")
		self.latex_file_button = QPushButton("Restore Default")
		self.latex_file_editor = views.editor.EditorView()
		self.latex_file_help = QLabel('<span style="font-size: 10pt; color: #555">Code placeholders: $PREAMBLE and $SOURCE</span>')
		self.preamble_label = QLabel("<b>Preamble used for new document:</b>")
		self.preamble_button = QPushButton("Restore Default")
		self.preamble_editor = views.editor.EditorView()

	def initView(self):
		self._initConnections()
		self._initWidgets()
		self._initLayout()
	
	def _initConnections(self):
		self.latex_file_editor.contentChangedSignal.connect(self._latexFileChanged)
		self.latex_file_button.clicked.connect(self._restoreDefaultTemplate)
		self.preamble_editor.contentChangedSignal.connect(self._preambleChanged)
		self.preamble_button.clicked.connect(self._restoreDefaultPreamble)
	
	def _initWidgets(self):
		self.latex_file_editor.initView(show_margin = False)
		self.preamble_editor.initView(show_margin = False)

	def _initLayout(self):
		layout = QGridLayout()
		layout.addWidget(self.latex_file_label, 0, 0, 1, 3)
		layout.addWidget(self.latex_file_editor, 1, 0, 1, 3)
		layout.addWidget(self.latex_file_help, 2, 0, 1, 2)
		layout.addWidget(self.latex_file_button, 2, 2)
		layout.addWidget(views.factory.ViewFactory.createLineSeparator(), 3, 0, 1, 3)
		layout.addWidget(self.preamble_label, 4, 0, 1, 3)
		layout.addWidget(self.preamble_editor, 5, 0, 1, 3)
		layout.addWidget(self.preamble_button, 6, 2)
		self.setLayout(layout)
	
	@property
	def preamble_template(self):
		return self.preamble_editor.content
	
	@preamble_template.setter
	def preamble_template(self, value):
		self.preamble_editor.content = value
	
	@property
	def latex_file_template(self):
		return self.latex_file_editor.content
	
	@latex_file_template.setter
	def latex_file_template(self, value):
		self.latex_file_editor.content = value
		
	def _restoreDefaultPreamble(self):
		self.preamble_editor.content = Preferences.defaultPreambleTemplate()
			
	def _restoreDefaultTemplate(self):
		self.latex_file_editor.content = Preferences.defaultLatexFileTemplate()
	
	def _latexFileChanged(self):
		self.latexFileTemplateChangedSignal.emit(self.latex_file_template)
	
	def _preambleChanged(self):
		self.preambleTemplateChangedSignal.emit(self.preamble_template)
