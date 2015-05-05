"""Test for 'upload' view."""

import unittest

from flask import Flask
from flask_login import LoginManager
from unittest import mock

from pagapp.views.upload import upload


class _FlaskApplicationContextTextCase(unittest.TestCase):
    """Parent for all tests of flask_wtf.Form and it's children.

    Make application context for running test."""

    def setUp(self):
        self.app = self.create_app()
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.client = self.app.test_client()
        self.ctx = self.app.test_request_context()
        self.ctx.push()
        self.lm = LoginManager()
        self.lm.init_app(self.app)

    def tearDown(self):
        self.ctx.pop()

    def create_app(self):
        app = Flask(__name__)
        app.secret_key = 'secret'
        return app


class UploadViewTestCase(_FlaskApplicationContextTextCase):
    """Test for 'upload' view.

    Test case:
    test_upload(): tests upload() function.
    """

    @mock.patch('pagapp.views.upload.render_template')
    def test_upload(self, mock_render_template):
        """Test for upload() function.

        Test case:
        Function should call render_template() in every cases.
        """
        render_template_result = 'Test123test'
        mock_render_template.return_value = render_template_result
        self.assertEqual(upload(), render_template_result,
                         msg="render_template() should be called.")


if __name__ == '__main__':
    unittest.main()
