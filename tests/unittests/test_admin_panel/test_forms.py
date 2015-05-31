"""Tests for admin's panel forms."""

import unittest
from unittest.mock import patch
from unittest.mock import MagicMock

from flask_wtf.form import ValidationError

from pagapp.admin_panel.forms import ChangePasswordForm
from pagapp.admin_panel.forms import UploadForm
from tests.unittests.flask_test import FlaskApplicationContextTestCase


class ChangePasswordFormTestCase(FlaskApplicationContextTestCase):
    """Tests for ChangePasswordForm.

    Test cases:
    test_validate_old_password() - tests for validate_old_password()
    function.
    """

    @patch('pagapp.admin_panel.forms.current_app')
    @patch('pagapp.admin_panel.forms.current_user')
    def test_validate_old_password(self, mock_current_user, mock_app):
        """Tests for validate_old_password() function.

        Test cases:
        If check_password() returned False - function should raise
        ValidationError.
        Else, function should not return anything.
        """
        test_data = 'test123test321'
        mock_form = MagicMock()
        mock_field = MagicMock()
        mock_field.data = test_data
        test_check_password_form = ChangePasswordForm()

        mock_current_user.check_password.return_value = True
        test_check_password_form.validate_old_password(mock_form, mock_field)

        mock_current_user.check_password.return_value = False
        self.assertRaises(ValidationError,
                          test_check_password_form.validate_old_password,
                          mock_form, mock_field)
        del mock_app


class UploadFormTestCase(FlaskApplicationContextTestCase):
    """Tests for UploadForm."""

    def test_validate_file_name_validated(self):
        """Test for validate_file_name() validator.

        Test case:
        If file name has allowed extension - function should ends normally
        without any exceptions.
        """
        path_to_app = 'pagapp.admin_panel.forms.current_app'
        with patch(path_to_app) as mock_app:
            mock_app.config = {'ALLOWED_EXTENSIONS': ['jpg', 'tiff']}
            mock_form = MagicMock()
            mock_field = MagicMock()
            mock_field.data.filename = 'test.jpg'
            UploadForm.validate_file_name(mock_form, mock_field)

    def test_validate_file_name_not_validated(self):
        """Test for validate_file_name() validator.

        Test case:
        If file name has not allowed extension - function should raise
        ValidationError exception.
        """
        path_to_app = 'pagapp.admin_panel.forms.current_app'
        with patch(path_to_app) as mock_app:
            mock_app.config = {'ALLOWED_EXTENSIONS': ['jpg', 'tiff']}
            mock_form = MagicMock()
            mock_field = MagicMock()
            mock_field.data.filename = 'test.txt'
            self.assertRaises(ValidationError, UploadForm.validate_file_name,
                              mock_form, mock_field)


if __name__ == '__main__':
    unittest.main()
