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

# Default user preferences
EDITOR_FONT = u'Monaco, Courrier,13,-1,5,50,0,0,0,1,0'
FILE_ENCODING = "UTF-8"   # UTF-8, LATIN-1
INDENTATION_TYPE = "spaces"  # tab, spaces
INDENTATION_SIZE = 4
AUTO_WRAP = True
SHOW_ERROR_MARKERS = True
SHOW_ERROR_ANNOTATIONS = True
SELECT_TAGS = False
PREVIEW_THRESHOLD = 500 # times in ms before previewing when the user stop typing
AUTO_PREVIEW = True

DEFAULT_PREAMBLE_TEMPLATE = u''
DEFAULT_TEMPLATE = u"""\\documentclass{article}
\\usepackage{tikz}
\\usepackage[graphics, active, tightpage]{preview}
\\PreviewEnvironment{tikzpicture}\n
$PREAMBLE\n
\\begin{document}
$SOURCE
\\end{document}"""

DEFAULT_LATEX_TO_PDF_COMMAND = u'pdflatex'
# placeholders: $OUTPUT_DIR, $FILE_NAME, $FILE_PATH
DEFAULT_LATEX_TO_PDF_ARGS = u'%s -file-line-error -interaction=nonstopmode -output-directory $OUTPUT_DIR -jobname $FILE_NAME $FILE_PATH'
DEFAULT_MAC_PDF_TO_IMAGE_COMMAND = u'sips'
# placeholders: $PDF_PATH, $IMAGE_PATH
DEFAULT_MAC_PDF_TO_IMAGE_ARGS = u'%s -s format png $PDF_PATH --out $IMAGE_PATH'
DEFAULT_PDF_TO_IMAGE_COMMAND = u'convert'
# placeholders: $PDF_PATH, $IMAGE_PATH
DEFAULT_PDF_TO_IMAGE_ARGS = u'%s -density 150 $PDF_PATH -quality 90 -transparent white $IMAGE_PATH'

SNIPPETS = {
	u'Draw': u'\\draw @@@;',
	u'Draw () -- ()': u'\\draw (@@@) -- ();',
	u'Node': u'\\node (@@@) {};',
	u'Fill': u'\\fill[@@@] ;',
	u'Filldraw': u'\\filldraw[fill=@@@, draw=] ;',
	u'Path': u'\\path @@@;',
	u'Foreach': u'\\foreach @@@ in {}',
	u'Foreach x': u'\\foreach \\x in {@@@}',
	u'Tabular': u"""\\begin{tabular}{@@@}
\end{tabular}"""
}
