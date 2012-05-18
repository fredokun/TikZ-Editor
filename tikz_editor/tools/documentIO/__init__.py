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

# The document IO tools are used for saving TikZ document onto the filesystem.

from reader import DocumentReader
from template import FileTemplate
from tags import *
from tikz_editor.tools import File


def readPreambleAndSourceFromFilePath(file_path):
	reader = DocumentReader(file_path)
	return reader.readPreambleAndSource()


def writeDocumentToFilePath(template, document, file_path):
	content = buildFileContentFromDocument(template, document)
	File.writeContentToFilePath(content, file_path)


def buildFileContentFromDocument(template, document):
	d = FileTemplate(template, document.preamble, document.source)
	return d.buildFileContent()


def getPreamblePositionFromSourceCode(latex_source):
	"""
	Returns the position (tuple of line indexes) of the preamble section in the given
	LaTeX source.
	"""
	return getSectionPositionFromSourceCodeAndTags(latex_source, PREAMBLE_BEGIN_TAG, PREAMBLE_END_TAG)


def getSourcePositionFromSourceCode(latex_source):
	"""
	Returns the position (tuple of line indexes) of the source section in the given LaTeX
	source.
	"""
	return getSectionPositionFromSourceCodeAndTags(latex_source, SOURCE_BEGIN_TAG, SOURCE_END_TAG)


def getSectionPositionFromSourceCodeAndTags(latex_source, begin_tag, end_tag):
	"""
	Returns the position of a section in LaTeX source code.
	The position is a tuple of line indexes and the section is identified by the given
	begin and end tags.
	"""
	assert latex_source is not None
	assert begin_tag and end_tag
	begin_line = 0
	end_line = 0
	i = 1
	lines = latex_source.split("\n")
	for line in lines:
		if line == begin_tag:
			begin_line = i + 1
		elif line == end_tag:
			end_line = i - 1
			break
		i += 1

	assert begin_line > 0 and end_line > 0 and begin_line <= end_line
	return (begin_line, end_line)

__all__ = ["readPreambleAndSourceFromFilePath", "writeDocumentToFilePath", "buildFileContentFromDocument"]
