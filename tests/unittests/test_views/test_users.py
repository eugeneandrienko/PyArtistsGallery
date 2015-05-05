"""Tests for pagapp.views.users module."""

import unittest

from flask import Flask
from flask_login import LoginManager
from unittest import mock
from sqlalchemy.orm.exc import ObjectDeletedError

from pagapp.views.users import login, logout, load_user, change_password


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


class _ObjectDeletedErrorState():
    """Fake class for state object for ObjectDeletedError exception."""

    @staticmethod
    def class_():
        pass

    @staticmethod
    def obj():
        pass


class UsersTestCase(_FlaskApplicationContextTextCase):
    """Tests for functions from pagapp.views.users module.

    Test cases:
    test_login() - test for login() function.
    test_change_password() - test for change_password() function.
    test_logout() - test for logout() function.
    test_load_user() - test for load_user() function.
    """

    @mock.patch('pagapp.views.users.render_template')
    @mock.patch('pagapp.views.users.flash')
    @mock.patch('pagapp.views.users.redirect')
    @mock.patch('pagapp.views.users.url_for')
    @mock.patch('pagapp.views.users.LoginForm')
    def test_login(self, mock_form, mock_url_for, mock_redirect,
                   mock_flash, mock_render_template):
        """Test for login() function.

        Test cases:
        If user's credentials is submitted - function should call redirect
        to /index.
        If user's credentials is not submitted and user enters some data in
        form's fields - function should execute flash() with error
        message and call render_template().
        If user's credentials is not submitted and user does not enters
        any data in form's fields - function should call render_template().
        """
        redirect_result = 'redirect'
        render_template = 'render_template'

        mock_render_template.return_value = render_template

        mock_form.return_value.validate_on_submit.return_value = True
        mock_url_for.return_value = 'test'
        mock_redirect.return_value = redirect_result
        self.assertEqual(login(), redirect_result,
                         msg="redirect() to /index called")

        mock_form.return_value.validate_on_submit.return_value = False
        mock_form.return_value.login.data = 'test'
        mock_form.return_value.password.data = None
        self.assertEqual(login(), render_template,
                         msg="render_template() should be called!")
        self.assertTrue(mock_flash.called,
                        msg="flash() with error message called")
        mock_flash.reset_mock()

        mock_form.return_value.login.data = None
        mock_form.return_value.password.data = 'test'
        self.assertEqual(login(), render_template,
                         msg="render_template() should be called!")
        self.assertTrue(mock_flash.called,
                        msg="flash() with error message called")
        mock_flash.reset_mock()

        mock_form.return_value.login.data = 'test'
        mock_form.return_value.password.data = 'test'
        self.assertEqual(login(), render_template,
                         msg="render_template() should be called!")
        self.assertTrue(mock_flash.called,
                        msg="flash() with error message called")
        mock_flash.reset_mock()

        mock_form.return_value.login.data = None
        mock_form.return_value.password.data = None
        self.assertEqual(login(), render_template,
                         msg="render_template() should be called!")
        self.assertFalse(mock_flash.called,
                         msg="flash() should not called")

    @mock.patch('pagapp.views.users.ChangePasswordForm')
    @mock.patch('pagapp.views.users.flash')
    @mock.patch('pagapp.views.users.render_template')
    def test_change_password(self, mock_render_template, mock_flash,
                             mock_change_password_form):
        """Test for change_password() function.

        Test cases:
        If form submit is validated - function should execute flash()
        and returns render_template().
        If form submit is not validated and we have some data entered in
        the form fields - we should execute flash with error message and
        return render_template().
        If form submit is not validated and we do not have any data in the
        form fields - we should just execute render_template().
        """
        render_template_result = 'render_template'

        mock_render_template.return_value = render_template_result
        mock_change_password_form.return_value.\
            validate_on_submit.return_value = True
        self.assertEqual(change_password(), render_template_result)
        mock_flash.assert_called_with(
            'Password successfully changed')
        mock_flash.reset_mock()

        mock_change_password_form.return_value.\
            validate_on_submit.return_value = False
        mock_change_password_form.return_value.\
            old_password.data = 1
        mock_change_password_form.return_value.\
            new_password.data = None
        mock_change_password_form.return_value.\
            new_password2.data = None
        self.assertEqual(change_password(), render_template_result)
        mock_flash.assert_called_with(
            'Cannot change password - something goes wrong!')
        mock_flash.reset_mock()

        mock_change_password_form.return_value.\
            old_password.data = None
        mock_change_password_form.return_value.\
            new_password.data = 1
        mock_change_password_form.return_value.\
            new_password2.data = None
        self.assertEqual(change_password(), render_template_result)
        mock_flash.assert_called_with(
            'Cannot change password - something goes wrong!')
        mock_flash.reset_mock()

        mock_change_password_form.return_value.\
            old_password.data = None
        mock_change_password_form.return_value.\
            new_password.data = None
        mock_change_password_form.return_value.\
            new_password2.data = 1
        self.assertEqual(change_password(), render_template_result)
        mock_flash.assert_called_with(
            'Cannot change password - something goes wrong!')
        mock_flash.reset_mock()

        mock_change_password_form.return_value.\
            new_password2.data = None
        self.assertEqual(change_password(), render_template_result)
        self.assertFalse(mock_flash.called,
                         msg="flash() should not be called!")

    @mock.patch('pagapp.views.users.url_for')
    @mock.patch('pagapp.views.users.redirect')
    @mock.patch('pagapp.views.users.logout_user')
    def test_logout(self, mock_url_for, mock_redirect, mock_logout_user):
        """Test for logout() function.

        Test cases:
        In every cases url_for(), redirect() and logout_user() should be
        called inside the function.
        """
        redirect_result = 'redirect_result'
        mock_url_for.return_value = 'test'
        mock_redirect.return_value = redirect_result
        self.assertEqual(logout(), redirect_result,
                         msg="redirect() should be called!")
        self.assertTrue(mock_logout_user.called,
                        msg="logout_user() should be called!")
        self.assertTrue(mock_url_for.called,
                        msg="url_for() should be called!")

    @mock.patch('pagapp.models.Users.query')
    def test_load_user(self, mock_query):
        """Test for load_user() function.

        Test cases:
        If User.query.get() returned some result without
        exception - load_user() should return this result.
        If User.query.get() failed with ObjectDeletedError
        exception - load_user() should return None.
        If User.query.get() failed with some another exception - load_user()
        should raise exception.
        """
        get_result = 'get_result'

        mock_query.get.return_value = get_result
        self.assertEqual(load_user(1), get_result,
                         msg="load_user() should returns get() result")

        mock_query.get.side_effect = ObjectDeletedError(
            _ObjectDeletedErrorState)
        self.assertEqual(load_user(1), None,
                         msg="load_user() should return None after"
                             "ObjectDeletedError")

        mock_query.get.side_effect = IndexError()
        self.assertRaises(IndexError, load_user, 1)


if __name__ == '__main__':
    unittest.main()
