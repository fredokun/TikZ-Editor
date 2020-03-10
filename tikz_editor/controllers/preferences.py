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

from tikz_editor.models import Preferences
from .errors import ErrorsController
from tikz_editor.views.editor import EditorView


class PreferencesController(QObject):
	"""
	Controller of the "Preferences" dialog. It basically connects and syncs user defaults
	with the preferences dialog.
	"""

	def __init__(self):
		super(PreferencesController, self).__init__()
		self.app_controller = None
		self.view = None

	def initController(self):
		assert self.view
		self._connectViewAndModel()
		self._syncViewAndModel()

	def _connectViewAndModel(self):
		self.view.editor.editorFontChangedSignal.connect(Preferences.setEditorFont)
		self.view.editor.fileEncodingChangedSignal.connect(Preferences.setFileEncoding)
		self.view.editor.lineEndingsChangedSignal.connect(Preferences.setLineEndings)
		self.view.editor.indentationTypeChangedSignal.connect(Preferences.setIndentationType)
		self.view.editor.indentationSizeChangedSignal.connect(Preferences.setIndentationSize)
		self.view.editor.autoWrapChangedSignal.connect(Preferences.setAutoWrap)
		self.view.editor.errorMarkersChangedSignal.connect(Preferences.setShowErrorMarkers)
		self.view.editor.errorAnnotationsChangedSignal.connect(Preferences.setShowErrorAnnotations)
		self.view.editor.selectTagsChangedSignal.connect(Preferences.setSelectTags)
		self.view.editor.autoPreviewChangedSignal.connect(Preferences.setAutoPreview)
		self.view.editor.previewThresholdChangedSignal.connect(Preferences.setPreviewThreshold)

		self.view.editor.editorFontChangedSignal.connect(EditorView.reloadUserPreferences)
		self.view.editor.fileEncodingChangedSignal.connect(EditorView.reloadUserPreferences)
		self.view.editor.lineEndingsChangedSignal.connect(EditorView.reloadUserPreferences)
		self.view.editor.indentationTypeChangedSignal.connect(EditorView.reloadUserPreferences)
		self.view.editor.indentationSizeChangedSignal.connect(EditorView.reloadUserPreferences)
		self.view.editor.autoWrapChangedSignal.connect(EditorView.reloadUserPreferences)
		self.view.editor.errorMarkersChangedSignal.connect(ErrorsController.reloadUserPreferences)
		self.view.editor.errorAnnotationsChangedSignal.connect(ErrorsController.reloadUserPreferences)
		self.view.editor.selectTagsChangedSignal.connect(EditorView.reloadUserPreferences)

		self.view.document.preambleTemplateChangedSignal.connect(Preferences.setPreambleTemplate)
		self.view.document.latexFileTemplateChangedSignal.connect(Preferences.setLatexFileTemplate)

		self.view.preview.previewTemplateChangedSignal.connect(Preferences.setPreviewTemplate)
		self.view.preview.latexToPDFCommandChangedSignal.connect(Preferences.setLatexToPDFCommand)
		self.view.preview.PDFToImageCommandChangedSignal.connect(Preferences.setPDFToImageCommand)

		self.view.snippets.snippetsChangedSignal.connect(Preferences.setSnippets)
		self.view.snippets.snippetsChangedSignal.connect(self.app_controller.loadSnippets)


	def _syncViewAndModel(self):
		self.view.editor.editor_font = Preferences.getEditorFont()
		self.view.editor.file_encoding = Preferences.getFileEncoding()
		self.view.editor.line_endings = Preferences.getLineEndings()
		self.view.editor.indentation_type = Preferences.getIndentationType()
		self.view.editor.indentation_size = Preferences.getIndentationSize()
		self.view.editor.auto_wrap = Preferences.getAutoWrap()
		self.view.editor.error_markers = Preferences.getShowErrorMarkers()
		self.view.editor.error_annotations = Preferences.getShowErrorAnnotations()
		self.view.editor.select_tags = Preferences.getSelectTags()
		self.view.editor.auto_preview = Preferences.getAutoPreview()
		self.view.editor.preview_threshold = Preferences.getPreviewThreshold()

		self.view.document.latex_file_template = Preferences.getLatexFileTemplate()
		self.view.document.preamble_template = Preferences.getPreambleTemplate()

		self.view.preview.preview_template = Preferences.getPreviewTemplate()
		self.view.preview.latex_to_pdf_command = Preferences.getLatexToPDFCommand()
		self.view.preview.pdf_to_image_command = Preferences.getPDFToImageCommand()

		self.view.snippets.snippets = Preferences.getSnippets()

	def showPreferences(self):
		self.view.show()
		self.view.raise_()
