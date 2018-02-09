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

APP_NAME = $(shell python tikz_editor/globals APPLICATION_NAME)
APP_VERSION = $(shell python tikz_editor/globals VERSION)
PYRCC = pyrcc4
DEPLOY_DIR = $(shell pwd)/deployment

all:
	@echo "Use one of the following targets:"
	@echo " install:    Run the Python installation script"
	@echo " clean:      Remove temporary build files"
	@echo " resources:  (dev) Build the PyQt resources module (dep. pyrcc4)"
	@echo " tgz:        (dev) Build a gzipped source archive with tar"
	@echo " app:        (dev) Build a Mac OS X APP bundle (dep. pyinstaller)"
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

# Build a gzipped source archive with tar
tgz: clean_tgz
	mkdir -p "tikz-editor_$(APP_VERSION)"
	cp -r tikz_editor tikz_editor.pyw \
		setup.py distribute_setup.py \
		LICENSE \
		"tikz-editor_$(APP_VERSION)/"
	cp $(DEPLOY_DIR)/tgz/README "tikz-editor_$(APP_VERSION)/"
	tar -zcvf "tikz-editor_$(APP_VERSION).tgz" "tikz-editor_$(APP_VERSION)"
	rm -rf "tikz-editor_$(APP_VERSION)"


# Build an Ubuntu DEB package
deb: clean_deb
	DEBFULLNAME="$(shell python tikz_editor/globals MAINTAINER)" \
	dh_make -s -n -r cdbs -c gpl2 \
		-e "$(shell python tikz_editor/globals EMAIL)" \
		-p "tikz-editor_$(APP_VERSION)" \
		-t $(DEPLOY_DIR)/deb

	rm -rf debian/*.ex
	rm -rf debian/README*

	debuild -us -uc


# Build a Mac OS X APP bundle
app: clean_app
	pip3 install sip PyQt5 qscintilla
	python3 ./setup.py py2app
	open dist

#####################
# Cleaning commands #
#####################

clean_setup:
	rm -rf *.egg-info
	rm -rf build
	rm -rf dist

clean_tgz:
	rm -rf tikz-editor_$(APP_VERSION)*

clean_deb:
	rm -rf debian
	rm -rf build
	rm -rf .pc

clean_app:
	rm -rf build
	rm -rf dist
	rm -f *.log
	rm -f *.spec

clean: clean_setup clean_tgz clean_deb clean_app
	find . -type f -name "*.pyc" -exec rm {} \;
	find . -name ".DS_Store" -exec rm -rf {} \;
