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

class PreviewPreferencesView(QWidget):
	"""
	The preview preferences view displays the user preferences for the previewing of
	TikZ figures.
	"""
	
	previewTemplateChangedSignal = pyqtSignal(unicode)
	latexToPDFCommandChangedSignal = pyqtSignal(unicode)
	PDFToImageCommandChangedSignal = pyqtSignal(unicode)
	
	def __init__(self, parent=None):
		super(PreviewPreferencesView, self).__init__(parent)
		self.app_controller = None
		
		self.preview_template_label = QLabel("<b>LaTeX file template used for previewing the document:</b>")
		self.preview_template_button = QPushButton("Restore Default")
		self.preview_template_editor = views.editor.EditorView()
		self.preview_template_help = QLabel('<span style="font-size: 10pt; color: #555">Code placeholders: $PREAMBLE and $SOURCE</span>')
		
		self.latex2pdf_label = QLabel("<b>Command used for typesetting the LaTeX source to PDF:</b>")
		self.latex2pdf_button = QPushButton("Restore Default")
		self.latex2pdf_text = QLineEdit()
		self.latex2pdf_help = QLabel('<span style="font-size: 10pt; color: #555">Placeholders: $OUTPUT_DIR, $FILE_NAME and $FILE_PATH</span>')
		
		self.pdf2image_label = QLabel("<b>Command used for converting the PDF preview to image:</b>")
		self.pdf2image_button = QPushButton("Restore Default")
		self.pdf2image_text = QLineEdit()
		self.pdf2image_help = QLabel('<span style="font-size: 10pt; color: #555">Placeholders: $PDF_PATH and $IMAGE_PATH</span>')

	def initView(self):
		self._initConnections()
		self._initWidgets()
		self._initLayout()
	
	def _initConnections(self):
		self.preview_template_editor.contentChangedSignal.connect(self._previewTemplateChanged)
		self.latex2pdf_text.textChanged.connect(self._latex2pdfChanged)
		self.pdf2image_text.textChanged.connect(self._pdf2imageChanged)
		self.preview_template_button.clicked.connect(self._restoreDefaultPreviewTemplate)
		self.latex2pdf_button.clicked.connect(self._restoreDefaultLatex2PDF)
		self.pdf2image_button.clicked.connect(self._restoreDefaultPDF2Image)
	
	def _initWidgets(self):
		self.preview_template_editor.initView(show_margin = False)

	def _initLayout(self):
		layout = QGridLayout()
		layout.addWidget(self.preview_template_label, 0, 0, 1, 3)
		layout.addWidget(self.preview_template_editor, 1, 0, 1, 3)
		layout.addWidget(self.preview_template_help, 2, 0, 1, 2)
		layout.addWidget(self.preview_template_button, 2, 2)
		layout.addWidget(views.factory.ViewFactory.createLineSeparator(), 3, 0, 1, 3)
		layout.addWidget(self.latex2pdf_label, 4, 0, 1, 3)
		layout.addWidget(self.latex2pdf_text, 5, 0, 1, 3)
		layout.addWidget(self.latex2pdf_help, 6, 0, 1, 2)
		layout.addWidget(self.latex2pdf_button, 6, 2)
		layout.addWidget(views.factory.ViewFactory.createLineSeparator(), 7, 0, 1, 3)
		layout.addWidget(self.pdf2image_label, 8, 0, 1, 3)
		layout.addWidget(self.pdf2image_text, 9, 0, 1, 3)
		layout.addWidget(self.pdf2image_help, 10, 0, 1, 2)
		layout.addWidget(self.pdf2image_button, 10, 2)		
		self.setLayout(layout)

	@property
	def preview_template(self):
		return self.preview_template_editor.content
	
	@preview_template.setter
	def preview_template(self, value):
		self.preview_template_editor.content = value
	
	@property
	def latex_to_pdf_command(self):
		return self.latex2pdf_text.text()
	
	@latex_to_pdf_command.setter
	def latex_to_pdf_command(self, value):
		self.latex2pdf_text.setText(value)
		self.latex2pdf_text.setCursorPosition(0)
		
	@property
	def pdf_to_image_command(self):
		return self.pdf2image_text.text()
	
	@pdf_to_image_command.setter
	def pdf_to_image_command(self, value):
		self.pdf2image_text.setText(value)
		self.pdf2image_text.setCursorPosition(0)
		
	def _restoreDefaultPreviewTemplate(self):
		self.preview_template_editor.content = Preferences.defaultPreviewTemplate()
	
	def _restoreDefaultLatex2PDF(self):
		self.latex2pdf_text.setText(Preferences.defaultLatexToPDFCommand())
	
	def _restoreDefaultPDF2Image(self):
		self.pdf2image_text.setText(Preferences.defaultPDFToImageCommand())
	
	def _previewTemplateChanged(self):
		self.previewTemplateChangedSignal.emit(self.preview_template)
	
	def _latex2pdfChanged(self):
		self.latexToPDFCommandChangedSignal.emit(self.latex_to_pdf_command)
	
	def _pdf2imageChanged(self):
		self.PDFToImageCommandChangedSignal.emit(self.pdf_to_image_command)