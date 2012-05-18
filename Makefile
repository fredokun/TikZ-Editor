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

PYRCC = pyrcc4

all: resources/__init__.py

# Builds the resources module using PyQt's pyrcc4.
# see: http://www.riverbankcomputing.co.uk/static/Docs/PyQt4/html/resources.html
resources/__init__.py: resources/resources.qrc
	$(PYRCC) -o $@ $<
