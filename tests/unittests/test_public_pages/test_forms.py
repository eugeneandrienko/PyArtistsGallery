"""Tests for forms included in public pages."""

import unittest
from unittest.mock import patch
from unittest.mock import MagicMock

from flask_wtf.form import ValidationError

from pagapp.public_pages.forms import LoginForm
from tests.unittests.flask_test import FlaskApplicationContextTestCase


class LoginFormTestCase(FlaskApplicationContextTestCase):
    """Tests for LoginForm class.

    Test case:
    test_validate_login(): tests for validate_login() method.
    test_validate_password(): tests for validate_password() method.
    """

    @patch('pagapp.public_pages.forms.Users')
    def test_validate_login(self, mock_users):
        """Tests for validate_login() method.

        Test cases:
        If filter_by() call returns valid user's object we shouldn't raise
        exceptions.
        If filter_by() class returns None - we should raise ValidationError
        exception.
        """
        test_data = 'test123test321'
        mock_field = MagicMock()
        test_login_form = LoginForm()
        filter_by_result = MagicMock()

        mock_field.data.return_value = test_data

        filter_by_result.first.return_value = test_data
        mock_users.query.filter_by.return_value = filter_by_result
        test_login_form.validate_login(None, mock_field)

        filter_by_result.first.return_value = None
        mock_users.query.filter_by.return_value = filter_by_result
        self.assertRaises(ValidationError, test_login_form.validate_login,
                          None, mock_field)

    @patch('pagapp.public_pages.forms.Users')
    def test_validate_password(self, mock_users):
        """Tests for validate_password() method.

        Test cases:
        If returned user is not None and password is valid - we should do
        nothing.
        If user is None - we should do nothing.
        If user is not None and password is invalid - we should raise
        ValidationError exception.
        """
        test_data = 'test12332123test'
        mock_form = MagicMock()
        mock_form.login.data.return_value = test_data
        mock_field = MagicMock()
        mock_field.data.return_value = test_data
        mock_user = MagicMock()
        test_login_form = LoginForm()
        filter_by_result = MagicMock()

        mock_user.check_password.return_value = True
        filter_by_result.first.return_value = mock_user
        mock_users.query.filter_by.return_value = filter_by_result
        test_login_form.validate_password(mock_form, mock_field)

        filter_by_result.first.return_value = None
        mock_users.query.filter_by.return_value = filter_by_result
        test_login_form.validate_password(mock_form, mock_field)

        mock_user.check_password.return_value = False
        filter_by_result.first.return_value = mock_user
        self.assertRaises(ValidationError, test_login_form.validate_password,
                          mock_form, mock_field)


if __name__ == '__main__':
    unittest.main()
