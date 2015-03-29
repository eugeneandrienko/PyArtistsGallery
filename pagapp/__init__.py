from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


# Contens of Python files in current directory:
# forms.py  - different forms for HTML pages
# models.py - descriptions for SQL tables (tables for user, album and picture
#             manage)
# views.py  - descriptions of URL paths (like /index) for current Python
#             software.


app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

from pagapp import views, models
