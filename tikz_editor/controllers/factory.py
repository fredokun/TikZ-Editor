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

from app import AppController
from about import AboutController
from document import DocumentController
from documents import DocumentsController
from preview import PreviewController
from errors import ErrorsController
from preferences import PreferencesController

from tikz_editor.models import DocumentFactory
from tikz_editor.views import ViewFactory


class ControllerFactory(object):
	"""
	Factory of all controllers.
	"""

	@staticmethod
	def createAppController():
		app_controller = AppController()
		app_controller.about_controller = ControllerFactory.createAboutController(app_controller)
		app_controller.documents_controller = ControllerFactory.createDocumentsController(app_controller)
		app_controller.preferences_controller = ControllerFactory.createPreferencesController(app_controller)
		app_controller.initController()
		return app_controller

	@staticmethod
	def createAboutController(app_controller):
		about_controller = AboutController()
		about_controller.app_controller = app_controller
		about_controller.view = ViewFactory.createAboutView(app_controller)
		about_controller.initController()
		return about_controller

	@staticmethod
	def createDocumentController(app_controller, file_path=None):
		doc_controller = DocumentController()
		doc_controller.app_controller = app_controller
		doc_view = ViewFactory.createDocumentView(app_controller, doc_controller)

		if file_path is None:
			doc_model = DocumentFactory.createEmptyDocument()
		else:
			doc_model = DocumentFactory.createDocumentFromFilePath(file_path)

		errors_controller = ControllerFactory.createErrorsController(app_controller, doc_controller, doc_view)
		doc_controller.errors_controller = errors_controller
		preview_controller = ControllerFactory.createPreviewController(app_controller, doc_controller, doc_view)
		doc_controller.preview_controller = preview_controller

		doc_controller.view = doc_view
		doc_controller.model = doc_model
		doc_controller.initController()
		return doc_controller

	@staticmethod
	def createErrorsController(app_controller, doc_controller, doc_view):
		errors_controller = ErrorsController()
		errors_controller.app_controller = app_controller
		errors_controller.doc_controller = doc_controller
		errors_controller.content_view = doc_view.content_view
		errors_controller.errors_view = doc_view.feedback_view.errors_view
		errors_controller.initController()
		return errors_controller

	@staticmethod
	def createPreviewController(app_controller, doc_controller, doc_view):
		preview_controller = PreviewController()
		preview_controller.app_controller = app_controller
		preview_controller.doc_controller = doc_controller
		preview_controller.preview_view = doc_view.preview_view
		preview_controller.initController()
		return preview_controller

	@staticmethod
	def createDocumentsController(app_controller):
		documents_controller = DocumentsController()
		documents_controller.app_controller = app_controller
		return documents_controller

	@staticmethod
	def createPreferencesController(app_controller):
		preferences_controller = PreferencesController()
		preferences_controller.app_controller = app_controller
		preferences_controller.view = ViewFactory.createPreferencesView(app_controller, preferences_controller)
		preferences_controller.initController()
		return preferences_controller
