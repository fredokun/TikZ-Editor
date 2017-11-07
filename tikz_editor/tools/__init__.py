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

import sys
from subprocess import Popen, PIPE
from .file import File, FileError
from .temp_dir import TemporaryDirectory, TemporaryDirectoryError

from PyQt5.QtWidgets import *


__all__ = ["File", "FileError", "TemporaryDirectory", "TemporaryDirectoryError"]


def isMacintoshComputer():
	return (sys.platform == 'darwin')


def isWindowsComputer():
	return (sys.platform in ('win32', 'cygwin'))


def findCommandLocation(command):
	"""
	Finds first found location of given command using "which".
	"""
	try:
		p = Popen(["which", command], stdout=PIPE)
		ret = p.communicate()
		command_path = ret[0].strip()
		if command_path == "":
			raise Exception()
		return command_path
	except Exception:
		return command


def addToClipboard(text):
	"""
	Adds the given argument to the system clipboard.
	"""
	QApplication.clipboard().setText(text)
