"""PyArtistsGallery configuration.

List of options:
GALLERY_TITLE -- title of the gallery, which shown on every page.
SQLALCHEMY_DATABASE_URI -- absolute path to SQLite database.
STATIC_FOLDER -- path to folder with css, js and other static files.
TEMPLATES_FOLDER -- path to folder with base templates.
"""

import os
import random
import string


_BASEDIR = os.path.abspath(os.path.dirname(__file__))


GALLERY_TITLE = 'TEST TITLE'

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(_BASEDIR, 'pagapp.db')

STATIC_FOLDER = os.path.join(_BASEDIR, 'static/')
TEMPLATES_FOLDER = os.path.join(_BASEDIR, 'templates/')


# Specific settings for Flask-WTForm. Do not edit!
WTF_CSRF_ENABLED = True
SECRET_KEY_LENGTH = 30
SECRET_KEY = ''.join(
    random.choice(
        string.ascii_letters + string.digits
    ) for _ in range(SECRET_KEY_LENGTH))
