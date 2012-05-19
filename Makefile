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
DEPLOY_DIR = $(shell pwd)/deployment

all:
	@echo "Use one of the following targets:"
	@echo " install:    Run the Python installation script"
	@echo " clean:      Remove temporary build files"
	@echo " resources:  (dev) Build the PyQt resources module (dep. pyrcc4)"
	@echo " deb:        (dev) Build an Ubuntu DEB package (dep. dh_make, debuild)"


# Alias to "python setup.py install"
install:
	python setup.py install --install-scripts=/usr/bin


########################
# Development commands #
########################

# Builds the resources module using PyQt's pyrcc4.
# see: http://www.riverbankcomputing.co.uk/static/Docs/PyQt4/html/resources.html
resources: tikz_editor/resources/__init__.py
tikz_editor/resources/__init__.py: tikz_editor/resources/resources.qrc
	$(PYRCC) -o $@ $<


#######################
# Deployment commands #
#######################

# Build an Ubuntu DEB package
deb: clean_deb
	DEBFULLNAME="$(shell python tikz_editor/globals MAINTAINER)" \
	dh_make -s -n -r cdbs -c gpl2 \
		-e "$(shell python tikz_editor/globals EMAIL)" \
		-p "tikz-editor_$(shell python tikz_editor/globals VERSION)" \
		-t $(DEPLOY_DIR)/deb

	rm -rf debian/*.ex
	rm -rf debian/README*

	debuild -us -uc


#####################
# Cleaning commands #
#####################

clean_setup:
	rm -rf *.egg-info
	rm -rf build
	rm -rf dist
	find . -type f -name "*.pyc" -exec rm {} \;

clean_deb:
	rm -rf debian
	rm -rf build
	rm -rf .pc

clean: clean_setup clean_deb
