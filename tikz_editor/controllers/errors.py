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

from tikz_editor.models import Preferences
from tikz_editor.tools import documentIO


class ConversionError(object):
	def __init__(self, line, error):
		super(ConversionError, self).__init__()
		self.line = line
		self.error = error

	def __str__(self):
		return self.error


class PreambleError(ConversionError):
	def __str__(self):
		error = self.error
		if self.line is not None:
			error = "(preamble l.%d) %s" % (self.line, error)
		return error


class SourceError(ConversionError):
	def __str__(self):
		error = self.error
		if self.line is not None:
			error = "(source l.%d) %s" % (self.line, error)
		return error


class ErrorsController(QObject):
	"""
	The errors controller populates the errors list and error feedbacks (margin markers
	and annotations).
	"""

	# list of instances used to reload preferences
	instances = []

	@staticmethod
	def reloadUserPreferences():
		for errors in ErrorsController.instances:
			errors.loadUserPreferences()

	def __init__(self):
		super(ErrorsController, self).__init__()
		self.app_controller = None
		self.doc_controller = None
		self.content_view = None
		self.errors_view = None
		self.errors = []
		self.show_error_markers = None
		self.show_error_annotations = None
		ErrorsController.instances.append(self)

	def initController(self):
		self.errors_view.errorSelectedSignal.connect(self.errorSelected)
		self.loadUserPreferences()

	def loadUserPreferences(self):
		self.show_error_markers = Preferences.getShowErrorMarkers()
		self.show_error_annotations = Preferences.getShowErrorAnnotations()
		self.clearErrorMarginMarkersAndAnnotations()
		self._updateEditorsMarginsAndAnnotations()

	def errorSelected(self, error):
		if isinstance(error, PreambleError):
			self.content_view.showPreambleView()
			self.content_view.preamble_editor_view.selectLine(error.line)
		else:
			self.content_view.showSourceView()
			line = error.line
			if not error.line:
				line = 1
			self.content_view.source_editor_view.selectLine(line)

	def converterErrorsOccurred(self, errors, latex_source):
		self.clearErrors()
		self._matchErrorsToSource(errors, latex_source)
		self._updateEditorsMarginsAndAnnotations()
		self._updateErrorsList()

	def clearErrors(self):
		self.errors = []
		self.errors_view.clearErrors()
		self.clearErrorMarginMarkersAndAnnotations()

	def clearErrorMarginMarkersAndAnnotations(self):
		self.content_view.source_editor_view.removeAllErrorMarginMarkers()
		self.content_view.source_editor_view.removeAllAnnotations()
		self.content_view.preamble_editor_view.removeAllErrorMarginMarkers()
		self.content_view.preamble_editor_view.removeAllAnnotations()

	def _matchErrorsToSource(self, errors, latex_source):
		"""
		Sorts errors between LaTeX sections (preamble and source) according to file
		template.
		"""
		(preamble_begin, preamble_end) = documentIO.getPreamblePositionFromSourceCode(latex_source)
		(source_begin, source_end) = documentIO.getSourcePositionFromSourceCode(latex_source)
		matched_errors = []
		for error in errors:
			line = error[0]
			message = error[1]
			if line is not None and line >= preamble_begin and line <= preamble_end:
				matched_errors.append(PreambleError(line - preamble_begin + 1, message))
			elif line is not None and line >= source_begin and line <= source_end:
				matched_errors.append(SourceError(line - source_begin + 1, message))
			elif line is not None and line > source_end:
				matched_errors.append(ConversionError(source_end - source_begin + 1, message))
			else:
				matched_errors.append(ConversionError(None, message))
		self.errors = matched_errors

	def _updateEditorsMarginsAndAnnotations(self):
		for error in self.errors:
			if isinstance(error, PreambleError):
				self._addErrorToViewMarginsAndAnnotations(self.content_view.preamble_editor_view, error)
			elif isinstance(error, SourceError) or isinstance(error, ConversionError):
				self._addErrorToViewMarginsAndAnnotations(self.content_view.source_editor_view, error)

	def _addErrorToViewMarginsAndAnnotations(self, view, error):
		line = error.line
		if not line:
			line = 1
		if self.show_error_markers:
			view.addErrorMarginMarkerToLine(line)
		if self.show_error_annotations:
			view.addAnnotationToLine(line, error.error)

	def _updateErrorsList(self):
		for error in self.errors:
			self.errors_view.addError(error)
