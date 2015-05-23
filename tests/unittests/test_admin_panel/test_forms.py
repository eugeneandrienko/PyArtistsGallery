"""Tests for admin's panel forms."""

import unittest
from unittest.mock import patch
from unittest.mock import MagicMock

from flask_wtf.form import ValidationError

from pagapp.admin_panel.forms import ChangePasswordForm
from pagapp.admin_panel.forms import AddAlbumForm
from tests.unittests.flask_test import FlaskApplicationContextTestCase


class ChangePasswordFormTestCase(FlaskApplicationContextTestCase):
    """Tests for ChangePasswordForm.

    Test cases:
    test_validate_old_password() - tests for validate_old_password()
    function.
    """

    @patch('pagapp.admin_panel.forms.current_user')
    def test_validate_old_password(self, mock_current_user):
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


class AddAlbumFormTestCase(FlaskApplicationContextTestCase):
    """Tests for AddAlbumForm.

    Test cases:
    test_validate_album_name() - test for validate_album_name()
    validator.
    """

    @patch('pagapp.admin_panel.forms.Albums')
    def test_validate_album_name(self, mock_albums):
        """Test for validate_album_name().

        Test cases:
        We should raise ValidationError if count of albums with album
        name == field.data is not zero.
        And else, we should not raise any exceptions.
        """
        mock_add_album_form = AddAlbumForm()
        mock_form = MagicMock()
        mock_field = MagicMock()
        mock_field.data = 'test'

        mock_albums.query.filter_by.return_value.count.return_value = 0
        mock_add_album_form.validate_album_name(mock_form, mock_field)

        mock_albums.query.filter_by.return_value.count.return_value = 1
        self.assertRaises(
            ValidationError, mock_add_album_form.validate_album_name,
            mock_form, mock_field)


if __name__ == '__main__':
    unittest.main()
