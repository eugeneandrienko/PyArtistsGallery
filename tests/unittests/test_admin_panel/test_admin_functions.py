"""Tests for administrator's functions from admin's panel."""

import string
import re
import unittest
from unittest.mock import patch
from unittest.mock import MagicMock

from pagapp.admin_panel.admin_functions import change_password, add_new_album


class ChangePasswordTestCase(unittest.TestCase):
    """Tests for change_password() function."""

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
            mock_form.submit_button.data = True
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

    def test_change_password_submission(self):
        """Test for change password.

        Test case:
        If form.submit_button.data is False we should immediately
        return from function.
        """
        mock_form = MagicMock()
        mock_form.submit_button.data = False
        change_password(mock_form)
        self.assertFalse(mock_form.validate.called)

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
        mock_form.submit_button.data = True
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
        mock_form.submit_button.data = True
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
        mock_form.submit_button.data = True
        mock_request.method = 'GET'
        change_password(mock_form)
        self.assertTrue(mock_flash_form_errors.called)


class AddNewAlbumTestCase(unittest.TestCase):
    """Tests for add_new_album() function."""

    def test_add_new_album_submission(self):
        """Test for add_new_album() function.

        Test case:
        If form is not submitted we should immediately
        return from function.
        """
        mock_form = MagicMock()
        mock_form.submit_button.data = False
        add_new_album(mock_form)
        self.assertFalse(mock_form.validate.called)

    @patch('pagapp.admin_panel.admin_functions.request')
    @patch('pagapp.admin_panel.admin_functions.flash_form_errors')
    def test_add_new_album_flash_errors(
            self, mock_flash_form_errors, mock_request):
        """Test for add_new_album() function.

        Test case:
        If form is submitted and not validated - function
        should call flash_form_errors() form.
        """
        mock_form = MagicMock()
        mock_form.submit_button.data = True
        mock_form.validate.return_value = False

        mock_request.method = 'POST'

        add_new_album(mock_form)
        self.assertTrue(mock_flash_form_errors.called)

    @patch('pagapp.admin_panel.admin_functions.Albums')
    def test_add_new_album(self, mock_albums):
        """Test for add_new_album() function.

        Test case:
        If form is submitted and validated - we should
        add new album in database. In this case URL of the album
        does not exists in the database.
        """
        path_to_request = 'pagapp.admin_panel.admin_functions.request'
        path_to_db = 'pagapp.admin_panel.admin_functions.db'
        path_to_flash = 'pagapp.admin_panel.admin_functions.flash'
        with patch(path_to_request) as mock_request, \
                patch(path_to_db) as mock_db, \
                patch(path_to_flash) as mock_flash:
            mock_form = MagicMock()
            mock_form.submit_button.data = True
            mock_form.validate.return_value = True
            mock_request.method = 'POST'

            test_album_name = 'Test Album name 1!'
            test_album_description = 'test album description'
            mock_form.album_name.data = test_album_name
            mock_form.album_description.data = test_album_description
            mock_albums.query.filter_by.return_value.count.return_value = 0

            url_part = test_album_name.lower()
            url_part = url_part.strip(string.punctuation)
            whitespace_re = re.compile('[' + string.whitespace + ']')
            url_part = whitespace_re.sub('-', url_part)

            add_new_album(mock_form)
            mock_albums.assert_called_with(
                url_part, test_album_name, test_album_description)

            del mock_db
            del mock_flash

    @patch('pagapp.admin_panel.admin_functions.random')
    @patch('pagapp.admin_panel.admin_functions.Albums')
    def test_add_new_album_url_exists(self, mock_albums, mock_random):
        """Test for add_new_album() function.

        Test case:
        If form is submitted and validated - we should
        add new album in database. In this case URL of the album
        exists in the database and we should add random string
        to the URL.
        """
        path_to_request = 'pagapp.admin_panel.admin_functions.request'
        path_to_db = 'pagapp.admin_panel.admin_functions.db'
        path_to_flash = 'pagapp.admin_panel.admin_functions.flash'
        with patch(path_to_request) as mock_request, \
                patch(path_to_db) as mock_db, \
                patch(path_to_flash) as mock_flash:
            mock_form = MagicMock()
            mock_form.submit_button.data = True
            mock_form.validate.return_value = True
            mock_request.method = 'POST'

            test_album_name = 'Test Album name 1!'
            test_album_description = 'test album description'
            mock_form.album_name.data = test_album_name
            mock_form.album_description.data = test_album_description
            mock_albums.query.filter_by.return_value.count.return_value = 1

            url_part = test_album_name.lower()
            url_part = url_part.strip(string.punctuation)
            whitespace_re = re.compile('[' + string.whitespace + ']')
            url_part = whitespace_re.sub('-', url_part)

            mock_random.choice.return_value = 'x'
            url_part += 'xxxxx'

            add_new_album(mock_form)
            mock_albums.assert_called_with(
                url_part, test_album_name, test_album_description)

            del mock_db
            del mock_flash


if __name__ == '__main__':
    unittest.main()
