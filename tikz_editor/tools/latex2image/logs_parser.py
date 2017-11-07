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

import re


class LogsParser(object):
	"""
	Extracts errors from pdflatex output logs
	"""

	ERROR_REGEXP = re.compile(r"^.*:(?P<line>[0-9]+): (?P<error>.+)$")
	UNDEFINED_CSEQ_REGEXP = re.compile(r".*(?P<seq>\\[^ ]*) ?$")

	def __init__(self):
		super(LogsParser, self).__init__()
		self._logs_lines = []
		self._errors = []

	@property
	def errors(self):
		return sorted(self._errors, key=lambda error: error[0] if error[0] is not None else 0)

	@errors.setter
	def errors(self, errors):
		self._errors = errors

	@property
	def logs(self):
		return "\n".join(self._logs_lines)

	@logs.setter
	def logs(self, logs):
		self._logs_lines = self._unwrapLogs(logs)

	def hasFoundErrors(self):
		return len(self._errors) > 0

	def isTypesettingAborted(self):
		logs = self.logs
		return "Fatal error occurred" in logs or "No pages of output." in logs

	def clearLogsAndErrors(self):
		self._logs_lines = []
		self._errors = []

	def addErrorMessage(self, message, line_number=None):
		error = (line_number, message)
		if error not in self._errors:
			self._errors.append(error)

	def parseErrorsFromLogs(self):
		match_error = None
		match_cseq = None
		waiting_undefined_control_sequence = False
		undefined_control_sequence_line = None

		for line in self._logs_lines:
			if line == "":
				continue

			if waiting_undefined_control_sequence:
				match_cseq = LogsParser.UNDEFINED_CSEQ_REGEXP.match(line)
				if match_cseq:
					error_message = "Undefined control sequence %s." % match_cseq.group("seq")
					self.addErrorMessage(error_message, undefined_control_sequence_line)
					waiting_undefined_control_sequence = False
					undefined_control_sequence_line = None

			elif line[0] == "!":
				self.addErrorMessage(line[2:], None)
				continue

			else:
				match_error = LogsParser.ERROR_REGEXP.match(line)
				if match_error:
					try:
						error_line = int(match_error.group("line"))
						error_message = match_error.group("error")

						if error_message == "Undefined control sequence.":
							undefined_control_sequence_line = error_line
							waiting_undefined_control_sequence = True
						else:
							self.addErrorMessage(error_message, error_line)
					except ValueError:
						pass

	def _unwrapLogs(self, logs):
		"""
		Returns the given logs after unwraping the lines
		"""
		unwrapped_logs = []
		lines = logs.split("\n")
		line_buffer = ""
		for line in lines:
			if self._isLineWrapped(line):
				line_buffer += line
				continue
			unwrapped_logs.append(line_buffer + line)
			line_buffer = ""
		return unwrapped_logs

	def _isLineWrapped(self, line):
		return (len(line) == 79)

	def getStyledLogs(self):
		"""
		Returns the logs with error message in red (HTML).
		"""
		styled_logs = []
		match = None
		for line in self._logs_lines:
			if line != "":
				match = LogsParser.ERROR_REGEXP.match(line)
				if match or line[0] == "!":
					line = '<span style="color: red;">%s</span>' % line
			styled_logs.append(line)

		return "<br/>".join(styled_logs)
