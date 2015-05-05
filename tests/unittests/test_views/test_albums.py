"""Tests for album-related views."""

import unittest

from flask import Flask
from unittest import mock

from pagapp.views.albums import album
from pagapp.views.albums import manage_albums
from pagapp.models import Albums


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

    def tearDown(self):
        self.ctx.pop()

    def create_app(self):
        app = Flask(__name__)
        app.secret_key = 'secret'
        return app


class AlbumsViewTestCase(_FlaskApplicationContextTextCase):
    """Tests for functions from pagapp.views.albums module.

    Test cases:
    test_album(): tests for album() function.
    test_manage_albums(): tests for manage_albums() function.
    """

    @mock.patch('pagapp.views.albums.GotoUploadFakeForm')
    @mock.patch('pagapp.views.albums.AlbumForm')
    @mock.patch('pagapp.views.albums.render_template')
    @mock.patch('pagapp.views.albums.url_for')
    @mock.patch('pagapp.views.albums.redirect')
    def test_album(self, mock_redirect, mock_url_for, mock_render_template,
                   mock_album_form, mock_goto_form,):
        """Tests for album() function with /album/<album_url> view

        Test cases:
        if user press submit button function should return
        rendered upload page.
        Else function should return rendered album's page for
        album with album's URL == album_url.
        """
        upload_test_redirect = 'upload_redirect'
        upload_test_render_template = 'upload_render_template'

        mock_goto_form.return_value.validate_on_submit.return_value = True
        mock_url_for.return_value = 'test'
        mock_redirect.return_value = upload_test_redirect
        self.assertEqual(album('test'), upload_test_redirect,
                         msg="Redirect to /upload did not happen!")
        self.assertTrue(mock_redirect.called,
                        msg="redirect() called.")

        mock_goto_form.return_value.validate_on_submit.return_value = False
        mock_album_form.return_value.matched_album.return_value = Albums(
            'test', 'test', 'test')
        mock_render_template.return_value = upload_test_render_template
        self.assertEqual(album('test'), upload_test_render_template,
                         msg="render_template() called!")

    @mock.patch('pagapp.views.albums.AddAlbumForm')
    @mock.patch('pagapp.views.albums.render_template')
    def test_manage_albums(self, mock_add_album_form, mock_render_template):
        """Test for manage_albums() function."""
        pass


if __name__ == '__main__':
    unittest.main()
