"""Blueprint with views for API calls."""

from flask import Blueprint

api = Blueprint('api', __name__, url_prefix='/api')

from pagapp.api.api import *
