"""Package with all, what necessary for gallery.

Contains description of application database, different
forms for gallery pages and handlers for various URLs.

List of modules:
forms -- contains forms for gallery pages.
models -- contains descriptions of tables for database.
views -- contains handler for application URLs.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

import pagapp.views

views.warning_killer()