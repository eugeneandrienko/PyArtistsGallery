import os

basedir = os.path.abspath(os.path.dirname(__file__))

GALLERY_TITLE = 'TEST TITLE'

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'pagapp.db')

# Specific settings for Flask-WTForm.
# Do not edit!
WTF_CSRF_ENABLED = True
SECRET_KEY = 'eWax6eighodie7aiFeed'