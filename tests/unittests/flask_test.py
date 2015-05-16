"""Helper classes for application's unittest."""

import unittest

from flask import Flask
from flask_login import LoginManager


class FlaskApplicationContextTestCase(unittest.TestCase):
    """Parent for all tests of flask_wtf.Form and it's children.

    Make application context for running test."""

    def setUp(self):
        self.lm = LoginManager()
        self.app = self.create_app()
        self.client = self.app.test_client()
        self.ctx = self.app.test_request_context()
        self.ctx.push()

    def tearDown(self):
        self.ctx.pop()

    def create_app(self):
        app = Flask(__name__)
        app.secret_key = 'secret'
        self.lm.init_app(app)
        return app
