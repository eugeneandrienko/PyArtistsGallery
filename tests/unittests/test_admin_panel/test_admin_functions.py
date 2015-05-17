"""Tests for administrator's functions from admin's panel."""

import unittest
from unittest.mock import patch
from unittest.mock import MagicMock

from pagapp.admin_panel.admin_functions import change_password


class ChangePasswordTestCase(unittest.TestCase):
    """Tests for administrator's functions from admin's panel."""

    @patch('pagapp.admin_panel.admin_functions.flash')
    @patch('pagapp.admin_panel.admin_functions.request')
    def test_change_password(self, mock_request, mock_flash):
        """Test for change_password().

        Test case:
        If request.method equals with 'POST' and form.validate() is True -
        we should set new password for current user and call flash()
        function with category = 'success'.
        """
        path_to_db = 'pagapp.admin_panel.admin_functions.db'
        path_to_current_user = 'pagapp.admin_panel.admin_functions.current_user'
        with patch(path_to_db) as mock_db, \
                patch(path_to_current_user) as mock_current_user:
            mock_db.session.commit.return_value = None
            mock_form = MagicMock()
            mock_form.new_password.data.return_value = None
            mock_form.validate.return_value = True
            mock_request.method = 'POST'
            change_password(mock_form)
            mock_current_user.set_new_password.assert_called_with(
                mock_form.new_password.data)

            self.assertTrue(mock_db.session.commit.called)
            self.assertTrue(mock_flash.called)
            mock_flash.assert_called_with('Password successfully changed',
                                          category='success')

    @patch('pagapp.admin_panel.admin_functions.flash_form_errors')
    @patch('pagapp.admin_panel.admin_functions.request')
    def test_change_password_not_post(self, mock_request,
                                      mock_flash_form_errors):
        """Test for change_password().

        Test case:
        If request.method not equals with 'POST' - we should call
        flash_form_errors() function.
        """
        mock_form = MagicMock()
        mock_form.validate.return_value = True
        mock_request.method = 'GET'
        change_password(mock_form)
        self.assertTrue(mock_flash_form_errors.called)

    @patch('pagapp.admin_panel.admin_functions.flash_form_errors')
    @patch('pagapp.admin_panel.admin_functions.request')
    def test_change_password_not_validated(self, mock_request,
                                           mock_flash_form_errors):
        """Tests for change_password().

        Test case:
        If form.validate() is not True - we should call flash_form_errors()
        function.
        """
        mock_form = MagicMock()
        mock_form.validate.return_value = False
        mock_request.method = 'POST'
        change_password(mock_form)
        self.assertTrue(mock_flash_form_errors.called)

    @patch('pagapp.admin_panel.admin_functions.flash_form_errors')
    @patch('pagapp.admin_panel.admin_functions.request')
    def test_change_password_not_post_not_valid(self, mock_request,
                                                mock_flash_form_errors):
        """Tests for change_password().

        Test case:
        If request.method not equals with 'POST' and form.validate() is
        not True - we should call flash_form_errors() function.
        """
        mock_form = MagicMock()
        mock_form.validate.return_value = False
        mock_request.method = 'GET'
        change_password(mock_form)
        self.assertTrue(mock_flash_form_errors.called)


if __name__ == '__main__':
    unittest.main()
