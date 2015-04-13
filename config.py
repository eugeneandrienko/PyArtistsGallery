"""PyArtistsGallery configuration.

List of options:
GALLERY_TITLE -- title of the gallery, which shown on every page.
SQLALCHEMY_DATABASE_URI -- absolute path to SQLite database.
"""

import os


_BASEDIR = os.path.abspath(os.path.dirname(__file__))

GALLERY_TITLE = 'TEST TITLE'

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(_BASEDIR, 'pagapp.db')

# Specific settings for Flask-WTForm. Do not edit!
WTF_CSRF_ENABLED = True
SECRET_KEY = 'eWax6eighodie7aiFeed'