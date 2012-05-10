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

from about import AboutView
from document import DocumentView
from document.content import ContentView
from document.preview import PreviewView
from document.feedback import FeedbackView
from document.feedback.logs import LogsView
from document.feedback.errors import ErrorsView
from document.properties import PropertiesView
from preferences import PreferencesView
from preferences.document import DocumentPreferencesView
from preferences.editor import EditorPreferencesView
from preferences.preview import PreviewPreferencesView
from preferences.snippets import SnippetsPreferencesView
from editor import EditorView

class ViewFactory(object):
	"""
	Factory of all views.
	"""
	
	@staticmethod
	def createAboutView(app_controller):
		about = AboutView()
		about.app_controller = app_controller
		about.initView()
		return about
		
	@staticmethod
	def createDocumentView(app_controller, doc_controller):
		doc = DocumentView()
		doc.app_controller = app_controller
		doc.doc_controller = doc_controller
		content = ViewFactory.createContentView(app_controller, doc)
		feedback = ViewFactory.createFeedbackView(app_controller, doc)
		preview = ViewFactory.createPreviewView(app_controller, doc)
		doc.content_view = content
		doc.feedback_view = feedback
		doc.preview_view = preview		
		doc.initView()
		return doc
	
	@staticmethod
	def createContentView(app_controller, parent=None):
		content = ContentView(parent)
		content.app_controller = app_controller
		content.source_editor_view = ViewFactory.createEditorView(app_controller, content)
		content.preamble_editor_view = ViewFactory.createEditorView(app_controller, content)
		content.initView()
		return content
	
	@staticmethod
	def createEditorView(app_controller, parent=None):
		editor = EditorView(parent)
		editor.app_controller = app_controller
		editor.initView()
		return editor
	
	@staticmethod
	def createFeedbackView(app_controller, parent=None):
		feedback = FeedbackView(parent)
		feedback.app_controller = app_controller
		feedback.errors_view = ViewFactory.createErrorsView(app_controller, feedback)
		feedback.logs_view = ViewFactory.createLogsView(app_controller, feedback)
		feedback.initView()
		return feedback
		
	@staticmethod
	def createLogsView(app_controller, parent=None):
		logs = LogsView(parent)
		logs.app_controller = app_controller
		logs.initView()
		return logs

	@staticmethod		
	def createErrorsView(app_controller, parent=None):
		errors = ErrorsView(parent)
		errors.app_controller = app_controller
		errors.initView()
		return errors
		
	@staticmethod
	def createPropertiesView(app_controller, parent=None):
		properties = PropertiesView(parent)
		properties.app_controller = app_controller
		properties.initView()
		return properties
	
	@staticmethod
	def createPreviewView(app_controller, parent=None):
		preview = PreviewView(parent)
		preview.app_controller = app_controller
		preview.figure_view = ViewFactory.createLabel(preview)
		return preview
	
	@staticmethod
	def createPreferencesView(app_controller, parent=None):
		preferences = PreferencesView()
		preferences.app_controller = app_controller
		preferences.document = ViewFactory.createDocumentPreferencesView(app_controller, preferences)
		preferences.editor = ViewFactory.createEditorPreferencesView(app_controller, preferences)
		preferences.preview = ViewFactory.createPreviewPreferencesView(app_controller, preferences)
		preferences.snippets = ViewFactory.createSnippetsPreferencesView(app_controller, preferences)
		preferences.initView()
		return preferences
	
	@staticmethod
	def createDocumentPreferencesView(app_controller, parent=None):
		document_pref = DocumentPreferencesView(parent)
		document_pref.app_controller = app_controller
		document_pref.initView()
		return document_pref
		
	@staticmethod
	def createEditorPreferencesView(app_controller, parent=None):
		editor_pref = EditorPreferencesView(parent)
		editor_pref.app_controller = app_controller
		editor_pref.initView()
		return editor_pref

	@staticmethod
	def createPreviewPreferencesView(app_controller, parent=None):
		preview_pref = PreviewPreferencesView(parent)
		preview_pref.app_controller = app_controller
		preview_pref.initView()
		return preview_pref
	
	@staticmethod
	def createSnippetsPreferencesView(app_controller, parent=None):
		snippets_pref = SnippetsPreferencesView(parent)
		snippets_pref.app_controller = app_controller
		snippets_pref.initView()
		return snippets_pref
		
	@staticmethod
	def createLabel(parent=None):
		return QLabel(parent)
	
	@staticmethod
	def createLineSeparator(parent=None):
		line = QFrame(parent)
		line.setFrameShape(QFrame.HLine)
		line.setFrameShadow(QFrame.Sunken)
		return line