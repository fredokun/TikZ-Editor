"""
This is a setup.py script generated by py2applet

Usage:
    python setup.py py2app
"""

from setuptools import setup

APP = ['tikz_editor.pyw']
DATA_FILES = []
OPTIONS = {'iconfile': 'deployment/mac/icon.icns'}

setup(
    name="Tikz Editor",
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
