"""Blueprint with public pages of application.

Contains Web pages and logic which should be accessible
for everyone in the Internet.

Contents:
pages -- Web pages for current blueprint module.
forms.py -- forms, which using in blueprint.
views.py -- views for current blueprint.
"""

from flask import Blueprint


public_pages = Blueprint('public_pages', __name__,
                         template_folder='pages',
                         static_folder='../static')


from pagapp.public_pages.views import *
