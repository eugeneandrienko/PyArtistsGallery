"""Tests for views for service pages."""

import unittest
from unittest.mock import patch
from unittest.mock import MagicMock
from jinja2 import TemplateNotFound

from pagapp.service_pages.views import first_run


class FirstRunTestCase(unittest.TestCase):
    """Tests for first_run() function.

    Test cases:
    test_first_run_false() - in normal case, if it is not
    a first run, user should be redirected to /index.
    """

    @patch('pagapp.service_pages.views.is_first_run')
    def test_first_run_false(self, mock_is_first_run):
        """Tests redirection to /index if it is not a first run."""
        mock_is_first_run.return_value = False
        path_to_redirect = 'pagapp.service_pages.views.redirect'
        path_to_url_for = 'pagapp.service_pages.views.url_for'
        with patch(path_to_redirect) as mock_redirect, \
                patch(path_to_url_for) as mock_url_for:
            redirect_result = 'test123'
            mock_url_for.return_value = 'test'
            mock_redirect.return_value = redirect_result
            self.assertEqual(first_run(), redirect_result,
                             msg="redirect() should be called")

    @patch('pagapp.service_pages.views.create_database')
    @patch('pagapp.service_pages.views.is_first_run')
    def test_first_run_true(self, mock_is_first_run, mock_create_database):
        """Tests, is database create on the first run of application.

        Test case:
        Database should be created if it is not a first execution of
        application.
        Data from configuration and users database should be successfully
        added to form.
        If request method is not POST - we should call flash_form_errors().
        render_template() should be called and returned successfully.
        """
        mock_is_first_run.return_value = True

        path_to_configuration = 'pagapp.service_pages.views.Configuration'
        path_to_users = 'pagapp.service_pages.views.Users'
        path_to_form = 'pagapp.service_pages.views.FirstRunForm'
        path_to_request = 'pagapp.service_pages.views.request'
        path_to_flash_form_errors = \
            'pagapp.service_pages.views.flash_form_errors'
        path_to_render_template = 'pagapp.service_pages.views.render_template'
        with patch(path_to_configuration) as mock_configuration, \
                patch(path_to_users) as mock_users, \
                patch(path_to_form) as mock_form, \
                patch(path_to_request) as mock_request, \
                patch(path_to_flash_form_errors) as mock_flash_form_errors, \
                patch(path_to_render_template) as mock_render_template:
            first_result = MagicMock()
            test_result = 'test1233321'
            render_template_result = 'test123'

            first_result.gallery_title = test_result
            first_result.nickname = test_result
            mock_configuration.query.first.return_value = first_result
            mock_users.query.first.return_value = first_result
            mock_form.gallery_title.data = 'test'
            mock_form.username.data = 'test'
            mock_request.method = 'GET'
            mock_render_template.return_value = render_template_result

            self.assertEqual(first_run(), render_template_result)
            self.assertTrue(mock_create_database.called)
            self.assertTrue(mock_flash_form_errors.called)

    @patch('pagapp.service_pages.views.create_database')
    @patch('pagapp.service_pages.views.is_first_run')
    def test_add_data_from_database(
            self, mock_is_first_run, mock_create_database):
        """Tests, how function add data from database.

        Test cases:
        If there are no necessary data in the database tables - function should
        not raise any exceptions and form fields should be left unchanged.
        """
        mock_is_first_run.return_value = True

        path_to_configuration = 'pagapp.service_pages.views.Configuration'
        path_to_users = 'pagapp.service_pages.views.Users'
        path_to_form = 'pagapp.service_pages.views.FirstRunForm'
        path_to_request = 'pagapp.service_pages.views.request'
        path_to_flash_form_errors = \
            'pagapp.service_pages.views.flash_form_errors'
        path_to_render_template = 'pagapp.service_pages.views.render_template'
        with patch(path_to_configuration) as mock_configuration, \
                patch(path_to_users) as mock_users, \
                patch(path_to_form) as mock_form, \
                patch(path_to_request) as mock_request, \
                patch(path_to_flash_form_errors) as mock_flash_form_errors, \
                patch(path_to_render_template) as mock_render_template:
            first_result = MagicMock()
            test_result = 'test1233321'
            render_template_result = 'test123'

            first_result.gallery_title = 'test'
            first_result.nickname = 'test'
            mock_configuration.query.first.side_effect = AttributeError()
            mock_users.query.first.side_effect = AttributeError()
            mock_form.gallery_title.data = test_result
            mock_form.username.data = test_result
            mock_request.method = 'GET'
            mock_render_template.return_value = render_template_result

            self.assertEqual(first_run(), render_template_result)
            self.assertTrue(mock_create_database.called)
            self.assertTrue(mock_flash_form_errors.called)
            self.assertEqual(mock_form.gallery_title.data, test_result)
            self.assertEqual(mock_form.username.data, test_result)

    @patch('pagapp.service_pages.views.Configuration')
    @patch('pagapp.service_pages.views.Users')
    def test_write_new_data_to_database(self, mock_users, mock_configuration):
        """Tests, how function write data from form to database.

        Test cases:
        If there are no data in the tables - function should write new
        data to the database and execute redirect() to /index.
        """
        path_to_create_database = 'pagapp.service_pages.views.create_database'
        path_to_is_first_run = 'pagapp.service_pages.views.is_first_run'
        path_to_request = 'pagapp.service_pages.views.request'
        path_to_form = 'pagapp.service_pages.views.FirstRunForm'
        path_to_db = 'pagapp.service_pages.views.db'
        path_to_redirect = 'pagapp.service_pages.views.redirect'
        path_to_url_for = 'pagapp.service_pages.views.url_for'
        with patch(path_to_is_first_run) as mock_is_first_run, \
                patch(path_to_create_database) as mock_create_database, \
                patch(path_to_request) as mock_request, \
                patch(path_to_form) as mock_form, \
                patch(path_to_db) as mock_db, \
                patch(path_to_redirect) as mock_redirect, \
                patch(path_to_url_for) as mock_url_for:
            mock_is_first_run.return_value = True
            mock_request.method = 'POST'
            mock_form.return_value.validate.return_value = True

            mock_configuration.query.first.side_effect = AttributeError()
            mock_users.query.first.side_effect = AttributeError()

            redirect_result = 'test_redirect_123'
            mock_redirect.return_value = redirect_result

            self.assertEqual(first_run(), redirect_result,
                             msg="redirect() should be called.")
            self.assertTrue(mock_db.session.add.called)
            self.assertTrue(mock_db.session.commit.called)
            del mock_create_database
            del mock_url_for

    @patch('pagapp.service_pages.views.create_database')
    @patch('pagapp.service_pages.views.is_first_run')
    def test_first_run_true(self, mock_is_first_run, mock_create_database):
        """Tests, is abort() called if template not found."""
        mock_is_first_run.return_value = True

        path_to_configuration = 'pagapp.service_pages.views.Configuration'
        path_to_users = 'pagapp.service_pages.views.Users'
        path_to_form = 'pagapp.service_pages.views.FirstRunForm'
        path_to_request = 'pagapp.service_pages.views.request'
        path_to_flash_form_errors = \
            'pagapp.service_pages.views.flash_form_errors'
        path_to_render_template = 'pagapp.service_pages.views.render_template'
        path_to_abort = 'pagapp.service_pages.views.abort'
        with patch(path_to_configuration) as mock_configuration, \
                patch(path_to_users) as mock_users, \
                patch(path_to_form) as mock_form, \
                patch(path_to_request) as mock_request, \
                patch(path_to_flash_form_errors) as mock_flash_form_errors, \
                patch(path_to_render_template) as mock_render_template, \
                patch(path_to_abort) as mock_abort:
            first_result = MagicMock()
            test_result = 'test1233321'

            first_result.gallery_title = test_result
            first_result.nickname = test_result
            mock_configuration.query.first.return_value = first_result
            mock_users.query.first.return_value = first_result
            mock_form.gallery_title.data = 'test'
            mock_form.username.data = 'test'
            mock_request.method = 'GET'
            mock_render_template.side_effect = TemplateNotFound(name='test')

            first_run()
            self.assertTrue(mock_abort.called,
                            msg="Should be called abort(404)!")
            self.assertTrue(mock_create_database.called)
            self.assertTrue(mock_flash_form_errors.called)


if __name__ == '__main__':
    unittest.main()
