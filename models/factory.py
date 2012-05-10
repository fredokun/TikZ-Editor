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

from document import DocumentModel

class DocumentFactory(object):
	"""
	Factory of document models.
	"""
	@staticmethod
	def createEmptyDocument():
		return DocumentModel()
	
	@staticmethod
	def createDocumentFromFilePath(file_path):
		assert file_path is not None
		d = DocumentModel(file_path)
		d.open()
		return d