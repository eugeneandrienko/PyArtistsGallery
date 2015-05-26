"""Tests for various support functions."""

from flask import Markup
import unittest
from unittest.mock import patch
from unittest.mock import MagicMock
from sqlalchemy.orm.exc import ObjectDeletedError
from sqlalchemy.exc import OperationalError

from pagapp.support_functions import load_user, flash_form_errors, \
    is_first_run, remove_danger_symbols


class LoadUserTestCase(unittest.TestCase):
    """Tests for load_user() function."""

    @patch('pagapp.support_functions.Users')
    def test_load_user(self, mock_users):
        """Test for load_user() function.

        Test case:
        Function should return Users.query.get() result if it do not
        raises ObjectDeletedError.
        """
        test_value = 'test1233321'
        mock_users.query.get.return_value = test_value
        self.assertEqual(load_user(1), test_value)

    @patch('pagapp.support_functions.Users')
    def test_load_user(self, mock_users):
        """Test for load_user() function.

        Test case:
        If Users.query.get() raises ObjectDeletedError - function should
        return None.
        """
        test_value = 'test1233321'
        mock_state = MagicMock()
        mock_state.class_.return_value = None
        mock_state.class_.__name__ = test_value
        mock_state.obj.return_value = None
        mock_users.query.get.side_effect = ObjectDeletedError(
            state=mock_state)
        self.assertEqual(load_user(1), None)


class FlashFormErrorsTestCase(unittest.TestCase):
    """Tests for flash_form_errors() function."""

    @patch('pagapp.support_functions.flash')
    def test_flash_form_errors(self, mock_flash):
        """Test for flash_form_errors() function.

        Test cases:
        Function should raise flash() for every error from errors array,
        for every errors array assigned with field.
        """
        mock_form = MagicMock()
        mock_form.errors.items.return_value = \
            [('field1', ['error1', 'error2', 'error3']),
             ('field2', ['error4', 'error5', 'error6']),
             ('field3', ['error7', 'error8', 'error9'])]
        flash_form_errors(mock_form)
        self.assertTrue(mock_flash.called, msg="flash() should be called!")


class IsFirstRunTestCase(unittest.TestCase):
    """Tests for is_first_run() function."""

    def test_is_first_run(self):
        """Test for normal execution of is_first_run().

        Test case:
        If all is ok and all database tables is
        existing - function should return False.
        """
        path_to_albums = 'pagapp.support_functions.Albums'
        path_to_configuration = 'pagapp.support_functions.Configuration'
        path_to_pictures = 'pagapp.support_functions.Pictures'
        path_to_users = 'pagapp.support_functions.Users'
        with patch(path_to_albums) as mock_albums, \
                patch(path_to_configuration) as mock_configuration, \
                patch(path_to_pictures) as mock_pictures, \
                patch(path_to_users) as mock_users:
            mock_configuration.query.all.return_value = ['test']
            mock_users.query.all.return_value = ['test']
            self.assertFalse(is_first_run())
            del mock_albums
            del mock_pictures

    def test_table_not_exists(self):
        """Test for is_next_run() with non-existent tables.

        Test case:
        If one table of database schema does not
        exists - function should return True.
        """
        path_to_albums = 'pagapp.support_functions.Albums'
        path_to_configuration = 'pagapp.support_functions.Configuration'
        path_to_pictures = 'pagapp.support_functions.Pictures'
        path_to_users = 'pagapp.support_functions.Users'
        with patch(path_to_albums) as mock_albums, \
                patch(path_to_configuration) as mock_configuration, \
                patch(path_to_pictures) as mock_pictures, \
                patch(path_to_users) as mock_users:
            mock_albums.query.first.side_effect = OperationalError(
                statement='test',
                params='test',
                orig='test')
            self.assertTrue(is_first_run())
            del mock_configuration
            del mock_pictures
            del mock_users

    def test_configuration_empty(self):
        """Test for is_first_run() with empty configuration."""
        path_to_albums = 'pagapp.support_functions.Albums'
        path_to_configuration = 'pagapp.support_functions.Configuration'
        path_to_pictures = 'pagapp.support_functions.Pictures'
        path_to_users = 'pagapp.support_functions.Users'
        with patch(path_to_albums) as mock_albums, \
                patch(path_to_configuration) as mock_configuration, \
                patch(path_to_pictures) as mock_pictures, \
                patch(path_to_users) as mock_users:
            mock_configuration.query.all.return_value = []
            self.assertTrue(is_first_run())
            del mock_albums
            del mock_pictures
            del mock_users

    def test_users_table_empty(self):
        """Test for is_first_run() with empty users table."""
        path_to_albums = 'pagapp.support_functions.Albums'
        path_to_configuration = 'pagapp.support_functions.Configuration'
        path_to_pictures = 'pagapp.support_functions.Pictures'
        path_to_users = 'pagapp.support_functions.Users'
        with patch(path_to_albums) as mock_albums, \
                patch(path_to_configuration) as mock_configuration, \
                patch(path_to_pictures) as mock_pictures, \
                patch(path_to_users) as mock_users:
            mock_users.query.all.return_value = []
            self.assertTrue(is_first_run())
            del mock_albums
            del mock_configuration
            del mock_pictures


class RemoveDangerSymbolsTestCase(unittest.TestCase):
    """Test(s) for remove_danger_symbols() function."""

    def test_remove_danger_symbols(self):
        test_string = '<test>string&=test?пример><</test>'
        expected_string = Markup(test_string).striptags()
        expected_string = Markup.escape(expected_string).__str__()
        self.assertEqual(remove_danger_symbols(test_string), expected_string)


if __name__ == '__main__':
    unittest.main()
