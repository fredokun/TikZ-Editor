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

from datetime import datetime

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from tikz_editor.models import Preferences
from tikz_editor.tools.latex2image import Converter, LatexToImageConversion
from tikz_editor.tools import documentIO
from tikz_editor.tools import TemporaryDirectory


class PreviewController(QObject):
	"""
	The preview controller converts when necessary or requested the document source to an
	image displayed in the preview view.
	"""
	willUpdatePreviewSignal = pyqtSignal()
	errorsInSourceSignal = pyqtSignal(list, str)
	logsSignal = pyqtSignal(str)

	def __init__(self):
		super(PreviewController, self).__init__()
		self.app_controller = None
		self.doc_controller = None
		self.preview_view = None
		self.latex2image_converter = None
		self.request_preview_update = False
		self.last_time_content_changed = datetime.now()

	def initController(self):
		temp_dir = TemporaryDirectory.get()
		self.latex2image_converter = Converter(temp_dir)
		self.latex2image_converter.convertedSignal.connect(self.previewGenerated)
		self.latex2image_converter.conversionAbortedSignal.connect(self.conversionAborted)

	@pyqtSlot(str)
	def documentContentChanged(self, content):
		self.last_time_content_changed = datetime.now()
		self.preview_view.showWaitingBackground()
		if not self.request_preview_update:
			self.requestPreviewUpdate()

	@pyqtSlot()
	def conversionAborted(self):
		self.preview_view.showErrorBackground()

	def requestPreviewUpdate(self):
		self.request_preview_update = True
		if self._isEndOfInstruction():
			self.updatePreview()
		else:
			self.updatePreviewAfterTypingPause()

	def _isEndOfInstruction(self):
		"""
		Returns whether the last typed character is a semi-colon, meaning the
		end of current TikZ instruction
		"""
		return (self.doc_controller.view.content_view.current_editor_view.getCharacterAtCurrentCursorPosition() == ";")

	def updatePreviewAfterTypingPause(self):
		"""
		Updates the preview when the user is making a pause while typing.
		"""
		if (datetime.now() - self.last_time_content_changed).microseconds >= 500000:
			self.updatePreview()
		else:
			QTimer.singleShot(400, self.updatePreviewAfterTypingPause)

	def updatePreview(self):
		self.request_preview_update = False
		doc = self.doc_controller.model
		template = Preferences.getPreviewTemplate()
		source = documentIO.buildFileContentFromDocument(template, doc)
		self.latex2image_converter.convertLatexToImage(source)

	def abortPreview(self):
		self.latex2image_converter.stopConversion()

	@pyqtSlot(LatexToImageConversion)
	def previewGenerated(self, conversion):
		self.willUpdatePreviewSignal.emit()
		if conversion.image_path:
			self.preview_view.figure = conversion.image_path
		self.preview_view.showNormalBackground()
		self.logsSignal.emit(conversion.logs)
		self.errorsInSourceSignal.emit(conversion.errors, conversion.source)
