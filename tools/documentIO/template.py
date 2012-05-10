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

from string import Template

from tags import *

class FileTemplate(object):
	"""
	The file template tool generates a full LaTeX/TikZ source from a template, preamble
	and source.
	"""
	def __init__(self, template, preamble, source):
		assert preamble is not None and source is not None
		super(FileTemplate, self).__init__()
		self.content = ""
		self.preamble = preamble
		self.source = source
		self.latex_template = Template(template)
			
	def buildFileContent(self):
		"""
		Builds the TikZ document with given preamble and source and the document template.
		"""
		self._buildPreambleChunk()
		self._buildSourceChunk()
		self._buildContentFromTemplate()
		return self.content
		
	def _buildPreambleChunk(self):
		self.preamble = "%s\n%s\n%s\n" % (PREAMBLE_BEGIN_TAG, self.preamble, PREAMBLE_END_TAG)
	
	def _buildSourceChunk(self):
		self.source = "%s\n%s\n%s\n" % (SOURCE_BEGIN_TAG, self.source, SOURCE_END_TAG)
	
	def _buildContentFromTemplate(self):
		self.content = TIKZ_TAG + "\n"
		self.content += self.latex_template.safe_substitute(PREAMBLE=self.preamble, SOURCE=self.source)
	