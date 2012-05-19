TikZ Editor
===========

TikZ Editor is a free code editor for the LaTeX graphic package TikZ.

![Main Window](http://github.com/mickael-menu/TikZ-Editor/wiki/images/screenshot1.png)


Features
--------

- Real-time preview of TikZ sources.
- Syntax highlighting for LaTeX/TikZ.
- Customizable code snippets.
- Feedback of LaTeX typesetting errors using source annotations and margin markers.
- Separated edition of TikZ source and LaTeX preamble.


Downloads
---------

 - [TikZ Editor 1.0 for Mac OS X](http://github.com/downloads/mickael-menu/TikZ-Editor/TikZ%20Editor-1.0.dmg) (10.6 Snow Leopard or higher)
 - [TikZ Editor 1.0 for Ubuntu Linux](http://github.com/downloads/mickael-menu/TikZ-Editor/tikz-editor_1.0_all.deb) (11.4 Natty Narwhal or higher)
 - [TikZ Editor 1.0 source archive](http://github.com/downloads/mickael-menu/TikZ-Editor/tikz-editor_1.0.tgz) (requires [Python v2.6+](http://www.python.org/), [PyQt v4.3+](http://www.riverbankcomputing.co.uk/software/pyqt), [QScintilla v2.6+](http://www.riverbankcomputing.com/software/qscintilla) and [ImageMagick](http://www.imagemagick.org/) on Windows/Linux)


License
-------

Copyright © 2012 Mickaël Menu

This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see <http://www.gnu.org/licenses/>.
(http://www.riverbankcomputing.com/software/qscintilla)

Versions:
	PyQt  >= 4.3
	Python >= 2.6

Mac OS X (with MacPorts):
	py26-qscintilla
	py26-pyqt4

Linux (with Ubuntu's apt-get):
	python-qt4
	python-qscintilla2
	imagemagick

	python-setuptools (pour dev)


To deploy on Mac OS X (with MacPorts):
	Avec py2app:
	py26-py2app

	OU avec pyinstaller:
	py26-altgraph
	py26-modulegraph
	1) inclure le module atexit dans les sources
	2) faire python pyinstaller.py -w (pour faire un .app) -y (pour supprimer le repertoire output sans ocnfirmation) /path/vers/source.py
