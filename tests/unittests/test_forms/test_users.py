"""Tests for LoginForm and PasswordForm."""

import unittest

from unittest import mock
from flask import Flask
from flask_login import LoginManager, AnonymousUserMixin
from flask_login import login_user

from pagapp.forms import LoginForm, ChangePasswordForm
from pagapp.models import Users


class _MockFilterByReturnValue():
    """Special mock object for filter_by() function.

    filter_by() function returns object with first() method.
    We use this method inside code of our application.
    """

    _first_return_value = None

    def __init__(self, first_return_value=None):
        self._first_return_value = first_return_value

    def first(self):
        """Special method, which uses inside code of out application."""
        return self._first_return_value


class _FlaskApplicationContextTestCase(unittest.TestCase):
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


class LoginFormTestCase(_FlaskApplicationContextTestCase):
    """Tests for LoginForm class.

    Test case:
    test_validate(): tests for validate() method.
    """

    @mock.patch('pagapp.forms.users.Users.query')
    @mock.patch('pagapp.forms.users.Users.check_password')
    @mock.patch('pagapp.forms.users.Form.validate')
    def test_validate(self, mock_validate, mock_check_password, mock_query):
        """Tests for _validate() method.

        Test cases:
        If Form.validate() return False we should return False too.
        If user not found in database, function should return False.
        If user's password is wrong - function should return False.
        Else we should return True.
        """
        test_login_form = LoginForm()
        mock_validate.return_value = False
        self.assertFalse(test_login_form.validate(),
                         msg="Form.validate() returned False!")
        mock_validate.return_value = True

        mock_query.filter_by.return_value = _MockFilterByReturnValue()
        self.assertFalse(test_login_form.validate(),
                         msg="User not found, we should get False!")

        mock_query.filter_by.return_value = _MockFilterByReturnValue(
            first_return_value=Users('test', 'test', 'test', True))
        mock_check_password.return_value = False
        self.assertFalse(test_login_form.validate(),
                         msg="User has wrong password!")

        mock_check_password.return_value = True
        self.assertTrue(test_login_form.validate(),
                        msg="User is exists and has right password.")


class ChangePasswordFormTestCase(_FlaskApplicationContextTestCase):
    """Tests for ChangePasswordForm class.

    Test cases:
    test_validate(): test for validate() method.
    """

    @mock.patch('pagapp.forms.users.Form.validate')
    @mock.patch('pagapp.forms.users.Users.check_password')
    def test_validate(self, mock_check_password, mock_validate):
        """Test for validate() method in ChangePasswordForm class.

        Test cases:
        If Form.validate() returned False we should return False too.
        If flask_login.current_user is None we should return False.
        If current_user.check_password() is False we should return False
        too.
        If fields new_password.data and new_password2.data are not equal
        we should return False.
        Else we should return True.
        """
        test_change_password = ChangePasswordForm()
        test_change_password.old_password.data = 'old password'
        test_change_password.new_password.data = 'new password'
        test_change_password.new_password2.data = 'new password'
        mock_validate.return_value = False
        self.assertFalse(test_change_password.validate(),
                         msg="Form.validate() returned False!")
        mock_validate.return_value = True

        login_user(AnonymousUserMixin())
        self.assertFalse(test_change_password.validate(),
                         msg="current_user is Anonymous!")
        login_user(Users('test', 'test', 'test', True))

        mock_check_password.return_value = False
        self.assertFalse(test_change_password.validate(),
                         msg="check_password() returned False!")
        mock_check_password.return_value = True

        test_change_password.new_password2.data = 'new password2'
        self.assertFalse(test_change_password.validate(),
                         msg="new_password != new_password2")
        test_change_password.new_password2.data = 'new password'

        self.assertTrue(test_change_password.validate())

if __name__ == '__main__':
    unittest.main()
