"""Tests for administrator's functions from admin's panel."""

import string
import re
import unittest
from unittest.mock import patch
from unittest.mock import MagicMock

from pagapp.admin_panel.admin_functions import change_password, add_new_album, \
    upload_files
from pagapp.support_functions import remove_danger_symbols


class ChangePasswordTestCase(unittest.TestCase):
    """Tests for change_password() function."""

    @patch('pagapp.admin_panel.admin_functions.current_app')
    @patch('pagapp.admin_panel.admin_functions.flash')
    @patch('pagapp.admin_panel.admin_functions.request')
    def test_change_password(self, mock_request, mock_flash, mock_app):
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
                remove_danger_symbols(mock_form.new_password.data))

            self.assertTrue(mock_db.session.commit.called)
            self.assertTrue(mock_flash.called)
            mock_flash.assert_called_with('Password successfully changed',
                                          category='success')
        del mock_app

    @patch('pagapp.admin_panel.admin_functions.current_app')
    def test_change_password_submission(self, mock_app):
        """Test for change password.

        Test case:
        If form.submit_button.data is False we should immediately
        return from function.
        """
        mock_form = MagicMock()
        mock_form.submit_button.data = False
        change_password(mock_form)
        self.assertFalse(mock_form.validate.called)
        del mock_app

    @patch('pagapp.admin_panel.admin_functions.current_app')
    @patch('pagapp.admin_panel.admin_functions.flash_form_errors')
    @patch('pagapp.admin_panel.admin_functions.request')
    def test_change_password_not_post(self, mock_request,
                                      mock_flash_form_errors, mock_app):
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
        del mock_app

    @patch('pagapp.admin_panel.admin_functions.current_app')
    @patch('pagapp.admin_panel.admin_functions.flash_form_errors')
    @patch('pagapp.admin_panel.admin_functions.request')
    def test_change_password_not_validated(self, mock_request,
                                           mock_flash_form_errors, mock_app):
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
        del mock_app

    @patch('pagapp.admin_panel.admin_functions.current_app')
    @patch('pagapp.admin_panel.admin_functions.flash_form_errors')
    @patch('pagapp.admin_panel.admin_functions.request')
    def test_change_password_not_post_not_valid(self, mock_request,
                                                mock_flash_form_errors,
                                                mock_app):
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
        del mock_app


class AddNewAlbumTestCase(unittest.TestCase):
    """Tests for add_new_album() function."""

    @patch('pagapp.admin_panel.admin_functions.current_app')
    def test_add_new_album_submission(self, mock_app):
        """Test for add_new_album() function.

        Test case:
        If form is not submitted we should immediately
        return from function.
        """
        mock_form = MagicMock()
        mock_form.submit_button.data = False
        add_new_album(mock_form)
        self.assertFalse(mock_form.validate.called)
        del mock_app

    @patch('pagapp.admin_panel.admin_functions.current_app')
    @patch('pagapp.admin_panel.admin_functions.request')
    @patch('pagapp.admin_panel.admin_functions.flash_form_errors')
    def test_add_new_album_flash_errors(
            self, mock_flash_form_errors, mock_request, mock_app):
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
        del mock_app

    @patch('pagapp.admin_panel.admin_functions.current_app')
    @patch('pagapp.admin_panel.admin_functions.Albums')
    def test_add_new_album(self, mock_albums, mock_app):
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
                remove_danger_symbols(url_part),
                remove_danger_symbols(test_album_name),
                remove_danger_symbols(test_album_description))

            del mock_db
            del mock_flash
        del mock_app

    @patch('pagapp.admin_panel.admin_functions.current_app')
    @patch('pagapp.admin_panel.admin_functions.random')
    @patch('pagapp.admin_panel.admin_functions.Albums')
    def test_add_new_album_url_exists(self, mock_albums, mock_random, mock_app):
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
            url_part = remove_danger_symbols(url_part)

            mock_random.choice.return_value = 'x'
            url_part += 'xxxxx'

            add_new_album(mock_form)
            mock_albums.assert_called_with(
                url_part,
                remove_danger_symbols(test_album_name),
                remove_danger_symbols(test_album_description))

            del mock_db
            del mock_flash
        del mock_app


class UploadFilesTestCase(unittest.TestCase):
    """Tests for upload_files() function."""

    def test_upload_files_submit_false(self):
        """Test for upload_files().

        Test case:
        If form is not submitted - function should return
        immediately. Before, it should update form.album.choices
        array anyway.
        Also, in this test checks form.album.choices updating.
        """
        mock_form = MagicMock()
        mock_form.submit_button.data = False

        path_to_albums = 'pagapp.admin_panel.admin_functions.Albums'
        with patch(path_to_albums) as mock_albums:
            mock_album = MagicMock()
            test_id = 1
            test_album_name = 'test1'
            mock_album.id = test_id
            mock_album.album_name = test_album_name
            mock_albums.query.all.return_value = [mock_album]

            upload_files(mock_form)
            self.assertEqual(mock_form.album.choices[0],
                             (str(test_id), test_album_name))

    @patch('pagapp.admin_panel.admin_functions.save_file')
    def test_upload_files(self, mock_save_file):
        """Test for upload_files().

        Test case:
        Form validated successfully - we should save file.
        """
        mock_form = MagicMock()
        mock_form.submit_button.data = True

        path_to_current_app = 'pagapp.admin_panel.admin_functions.current_app'
        path_to_albums = 'pagapp.admin_panel.admin_functions.Albums'
        path_to_request = 'pagapp.admin_panel.admin_functions.request'
        with patch(path_to_current_app) as mock_current_app, \
                patch(path_to_albums) as mock_albums, \
                patch(path_to_request) as mock_request:
            mock_album = MagicMock()
            test_id = 1
            test_album_name = 'test1'
            mock_album.id = test_id
            mock_album.album_name = test_album_name
            mock_albums.query.all.return_value = [mock_album]

            mock_request.method = 'POST'
            mock_current_app.config['UPLOAD_FOLDER'] = 'test'
            upload_files(mock_form)
            self.assertTrue(mock_save_file.called)

    def test_upload_files_not_valid(self):
        """Test for upload_files().

        Test case:
        Form not validated or request.method is not 'POST' or both.
        Logger function debug() should be called and flash_form_errors()
        should be called too.
        """
        mock_form = MagicMock()
        mock_form.submit_button.data = True

        path_to_current_app = 'pagapp.admin_panel.admin_functions.current_app'
        path_to_flash_form_errors = \
            'pagapp.admin_panel.admin_functions.flash_form_errors'
        path_to_albums = 'pagapp.admin_panel.admin_functions.Albums'
        path_to_request = 'pagapp.admin_panel.admin_functions.request'
        with patch(path_to_current_app) as mock_current_app, \
                patch(path_to_flash_form_errors) as mock_flash_form_errors, \
                patch(path_to_albums) as mock_albums, \
                patch(path_to_request) as mock_request:
            mock_album = MagicMock()
            test_id = 1
            test_album_name = 'test1'
            mock_album.id = test_id
            mock_album.album_name = test_album_name
            mock_albums.query.all.return_value = [mock_album]

            mock_request.method = 'GET'
            upload_files(mock_form)
            self.assertTrue(mock_current_app.logger.debug.called)
            self.assertTrue(mock_flash_form_errors.called)


if __name__ == '__main__':
    unittest.main()
