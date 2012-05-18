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

import tempfile
import shutil


class TemporaryDirectoryError(Exception):
	pass


class TemporaryDirectory(object):
	"""
	Temporary Directory is a tool to generates an application-wide temporary directory.
	Don't forget to delete it using TemporaryDirectory.delete() when the application quits.
	"""
	temporary_directory = None

	@staticmethod
	def get():
		if not TemporaryDirectory.temporary_directory:
			TemporaryDirectory.generate()
		return TemporaryDirectory.temporary_directory

	@staticmethod
	def generate():
		try:
			TemporaryDirectory.temporary_directory = tempfile.mkdtemp(prefix="tikz_")
		except Exception, e:
			raise TemporaryDirectoryError("Can't create a temporary directory: %s" % str(e))

	@staticmethod
	def delete():
		try:
			if TemporaryDirectory.temporary_directory is not None:
				shutil.rmtree(TemporaryDirectory.temporary_directory)
		except Exception:
			pass
