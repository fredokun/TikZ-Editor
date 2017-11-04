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
from PyQt5.QtWidgets import *


from tikz_editor.tools import isMacintoshComputer
from tikz_editor.tools.qt import Dialogs
from tikz_editor.models import Preferences
import tikz_editor.views.editor
import tikz_editor.views.factory


class EditSnippetView(QDialog):
	"""
	Dialog for editing a snippet.
	"""

	def __init__(self, parent, snippets_view, name=None, code=None):
		super(EditSnippetView, self).__init__(parent)
		self.old_name = name
		self.old_code = code
		self.snippets_view = snippets_view
		self.name_label = QLabel("<b>Name:</b>")
		self.name_edit = QLineEdit()
		self.code_label = QLabel("<b>Code:</b>")
		self.code_edit = tikz_editor.views.editor.EditorView()
		self.code_help = QLabel('<span style="font-size: 10pt; color: #555">Cursor position placeholder: @@@</span>')
		self.cancel_button = QPushButton("Cancel")
		self.ok_button = QPushButton("OK")
		self.initDialog()

	def dialogTitle(self):
		return "Edit Snippet"

	@property
	def name(self):
		return str(self.name_edit.text(), 'utf-8')

	@name.setter
	def name(self, name):
		self.name_edit.setText(name)

	@property
	def code(self):
		return str(self.code_edit.content, 'utf-8')

	@code.setter
	def code(self, code):
		self.code_edit.content = code

	def initDialog(self):
		self.name = self.old_name
		self.code = self.old_code
		self.setWindowTitle(self.dialogTitle())
		if isMacintoshComputer():
			self.setWindowFlags(Qt.Sheet)
		else:
			self.setModal(True)
		self._initConnections()
		self._initWidgets()
		self._initLayout()

	def _initConnections(self):
		self.cancel_button.clicked.connect(self._cancelClicked)
		self.ok_button.clicked.connect(self._okClicked)

	def _initWidgets(self):
		self.code_edit.initView(show_margin=False)
		self.ok_button.setDefault(True)

	def _initLayout(self):
		layout = QVBoxLayout()
		layout.addWidget(self.name_label)
		layout.addWidget(self.name_edit)
		layout.addWidget(self.code_label)
		layout.addWidget(self.code_edit)
		layout.addWidget(self.code_help)
		sublayout = QHBoxLayout()
		sublayout.addWidget(self.cancel_button, 1, Qt.AlignRight)
		sublayout.addWidget(self.ok_button, 0, Qt.AlignRight)
		layout.addLayout(sublayout)
		self.setLayout(layout)

	def _okClicked(self):
		snippets = self.snippets_view.snippets
		if self.name.strip() == u"":
			Dialogs.showError("The snippet name is empty")
		elif self.code.strip() == u"":
			Dialogs.showError("The snippet code is empty")
		elif self.old_name != self.name and self.name in snippets:
			Dialogs.showError("A snippet with the same name already exists")
		else:
			if self.old_name != self.name:
				del snippets[self.old_name]
			snippets[self.name] = self.code
			self.snippets_view.snippets = snippets
			self.snippets_view.snippetsChangedSignal.emit(snippets)
			self.close()

	def _cancelClicked(self):
		self.close()


class AddSnippetView(EditSnippetView):
	"""
	Dialog for adding a snippet.
	"""

	def __init__(self, parent, snippets_view):
		super(AddSnippetView, self).__init__(parent, snippets_view, u"Untitled", u"")

	def dialogTitle(self):
		return "Add Snippet"

	def _okClicked(self):
		snippets = self.snippets_view.snippets
		if self.name.strip() == u"":
			Dialogs.showError("The snippet name is empty")
		elif self.code.strip() == u"":
			Dialogs.showError("The snippet code is empty")
		elif self.name in snippets:
			Dialogs.showError("A snippet with the same name already exists")
		else:
			snippets[self.name] = self.code
			self.snippets_view.snippets = snippets
			self.snippets_view.snippetsChangedSignal.emit(snippets)
			self.close()


class SnippetsPreferencesView(QWidget):
	"""
	The snippets preferences view displays the user preferences for the editor snippets.
	"""

	snippetsChangedSignal = pyqtSignal(dict)

	def __init__(self, parent=None):
		super(SnippetsPreferencesView, self).__init__(parent)
		self.app_controller = None

		self.snippets_label = QLabel("<b>Code Snippets:</b>")
		self.snippets_list = QTreeWidget()
		self.reset_button = QPushButton("Restore All Snippets")
		self.add_button = QPushButton("Add")
		self.remove_button = QPushButton("Remove")
		self.edit_button = QPushButton("Edit")
		self._snippets = {}

	def initView(self):
		self._initConnections()
		self._initWidgets()
		self._initLayout()

	def _initConnections(self):
		self.snippets_list.itemDoubleClicked.connect(self._snippetDoubleClicked)
		self.reset_button.clicked.connect(self._restoreAllSnippets)
		self.add_button.clicked.connect(self._addSnippet)
		self.remove_button.clicked.connect(self._removeSnippet)
		self.edit_button.clicked.connect(self._editSnippet)

	def _initWidgets(self):
		self.snippets_list.setMinimumHeight(350)
		self.snippets_list.setColumnCount(2)
		self.snippets_list.setHeaderLabels(["Name", "Code"])
		self.snippets_list.setSortingEnabled(True)
		self.snippets_list.sortByColumn(0, Qt.AscendingOrder)
		self.snippets_list.setSelectionBehavior(QTreeWidget.SelectRows)
		self.snippets_list.setSelectionMode(QTreeWidget.ExtendedSelection)

	def _initLayout(self):
		layout = QVBoxLayout()
		layout.addWidget(self.snippets_label)
		layout.addWidget(self.snippets_list)
		sublayout = QHBoxLayout()
		sublayout.addWidget(self.add_button, 0, Qt.AlignLeft)
		sublayout.addWidget(self.remove_button, 0, Qt.AlignLeft)
		sublayout.addWidget(self.edit_button, 0, Qt.AlignLeft)
		sublayout.addWidget(self.reset_button, 1, Qt.AlignRight)
		layout.addLayout(sublayout)
		self.setLayout(layout)

	def editSnippet(self, snippet):
		if snippet in self.snippets:
			code = self.snippets[snippet]
			edit_dialog = EditSnippetView(self.parent(), self, snippet, code)
			edit_dialog.show()
		else:
			Dialogs.showError("Can't edit the snippet \"%s\": the snippet doesn't exist")

	def removeSnippet(self, snippet):
		if snippet in self.snippets:
			del self.snippets[snippet]
			self._updateSnippetsListView()
			self.snippetsChangedSignal.emit(self.snippets)
		else:
			Dialogs.showError("Can't remove the snippet \"%s\": the snippet doesn't exist")

	@property
	def selected_snippets(self):
		selected_snippets = []
		items = self.snippets_list.selectedItems()
		for item in items:
			selected_snippets.append(str(item.data(0, Qt.DisplayRole).toString(),'utf-8'))
		return selected_snippets

	@property
	def snippets(self):
		return self._snippets

	@snippets.setter
	def snippets(self, snippets):
		self._snippets = snippets
		self._updateSnippetsListView()

	def _updateSnippetsListView(self):
		self.snippets_list.clear()
		if self.snippets is not None:
			items = []
			for (name, code) in self.snippets.items():
				code = code.replace('\n', ' ')
				item = QTreeWidgetItem([name, code])
				item.setData(0, Qt.DisplayRole, name)
				items.append(item)
			self.snippets_list.insertTopLevelItems(0, items)

	def _snippetDoubleClicked(self, item, column):
		self.editSnippet(str(item.data(0, Qt.DisplayRole).toString(),'utf-8'))

	def _restoreAllSnippets(self):
		self.snippets = Preferences.defaultSnippets()
		self.snippetsChangedSignal.emit(self.snippets)

	def _addSnippet(self):
		dialog = AddSnippetView(self.parent(), self)
		dialog.show()

	def _removeSnippet(self):
		for snippet in self.selected_snippets:
			self.removeSnippet(snippet)

	def _editSnippet(self):
		selected_snippets = self.selected_snippets
		if len(selected_snippets) > 0:
			self.editSnippet(selected_snippets[0])
