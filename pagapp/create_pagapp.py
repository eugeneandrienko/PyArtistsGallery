"""Functions which instantiate web application."""

from flask import Flask

from pagapp.models import db
from pagapp.support_functions import lm
from pagapp.public_pages import public_pages
from pagapp.admin_panel import admin_panel
from pagapp.service_pages import service_pages


def create_pagapp(path_to_config):
    """Flask application creator.

    Creates PyArtistsGallery application with configuration,
    red from given path_to_config.
    """
    app = Flask(__name__)
    app.config.from_object(path_to_config)
    app.static_folder = app.config['STATIC_FOLDER']
    app.template_folder = app.config['TEMPLATES_FOLDER']

    db.init_app(app)
    lm.init_app(app)

    app.register_blueprint(public_pages)
    app.register_blueprint(admin_panel)
    app.register_blueprint(service_pages)

    return app
