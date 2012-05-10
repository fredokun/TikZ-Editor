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

class LogsView(QTextEdit):	
	"""
	The logs view displays pdf2image converter logs.
	"""
	def __init__(self, parent=None):
		super(LogsView, self).__init__(parent)
		self.app_controller = None
	
	def initView(self):
		self.setReadOnly(True)
	
	def clearLogs(self):
		self.clear()
		
	def setLogs(self, logs):
		self.setHtml(logs)
		self.scrollToEnd()
	
	def scrollToEnd(self):
		self.moveCursor(QTextCursor.End)