import os
basedir = os.path.abspath(os.path.dirname(__file__))

GALLERY_TITLE = 'TEST TITLE'

WTF_CSRF_ENABLED = True
SECRET_KEY = 'eWax6eighodie7aiFeed'

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'pagapp.db')
SQLALCHEMY_DATABASE_REPO = os.path.join(basedir, 'db_repository')
