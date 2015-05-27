"""Tests for API calls."""

from flask_login import login_user
import json
import unittest
from unittest.mock import patch
from unittest.mock import MagicMock

from pagapp.models.users import Users
from pagapp.application_api.album_api import get_albums_list, delete_album, \
    edit_album
from tests.unittests.flask_test import FlaskApplicationContextTestCase


class GetAlbumsListTestCase(unittest.TestCase):
    """Tests for /api/get-albums-list API call."""

    @patch('pagapp.application_api.album_api._generate_album_table_item')
    @patch('pagapp.application_api.album_api.Pictures')
    @patch('pagapp.application_api.album_api.Albums')
    def test_get_albums_list(self, mock_albums, mock_pictures,
                             mock_generate_album_table_item):
        """Test for /api/get-album-list API call.

        Test case:
        In every case we should return json with list
        of albums.
        """
        login_user(Users('nickname', 'password', True))
        mock_album = MagicMock()
        mock_album.album_name = 'test_name'
        mock_album.album_description = 'test description'
        mock_album.id = 1

        mock_pictures.query.filter_by.return_value.count.return_value = 1
        mock_generate_album_table_item.return_value = {'test1': 'test2'}

        mock_albums.query.all.return_value = [mock_album]

        expected_result = json.dumps(
            [
                {
                    'test1': 'test2'
                }
            ]
        )

        self.assertEqual(get_albums_list(), expected_result)


class DeleteAlbumTestCase(FlaskApplicationContextTestCase):
    """Tests for delete_album() function."""

    @patch('pagapp.application_api.album_api.current_app')
    @patch('pagapp.application_api.album_api.request')
    @patch('pagapp.application_api.album_api.Albums')
    def test_delete_album(self, mock_albums, mock_request, mock_app):
        """Test for /delete-album API call.

        Test cases:
        If count of albums with given id is not equal with one - function
        should return tuple ('', 404).
        Else, if count of albums equals with one - function should
        return tuple ('', 200).
        """
        login_user(Users('nickname', 'password', True))

        mock_album = MagicMock()
        mock_album.first.return_value = 'test'
        mock_album.count.return_value = 2
        mock_albums.query.filter_by.return_value = mock_album
        self.assertEqual(delete_album(), ('', 404))

        with patch('pagapp.application_api.album_api.db') as mock_db:
            mock_album.count.return_value = 1
            mock_albums.query.filter_by.return_value = mock_album
            self.assertEqual(delete_album(), ('', 200))
            del mock_db
        del mock_request
        del mock_app


class EditAlbumTestCase(FlaskApplicationContextTestCase):
    """Tests for /api/edit-album API call."""

    @patch('pagapp.application_api.album_api.current_app')
    @patch('pagapp.application_api.album_api.db')
    @patch('pagapp.application_api.album_api.request')
    @patch('pagapp.application_api.album_api.Albums')
    def test_edit_album(self, mock_albums, mock_request, mock_db, mock_app):
        """Test for edit_album() function.

        Test cases:
        If count of albums with given ID is not equal with one - function
        should return 404 error.
        Otherwise it should rename album and return code 200.
        """
        login_user(Users('nickname', 'password', True))
        mocked_album = MagicMock()

        mocked_album.count.return_value = 0
        mock_albums.query.filter_by.return_value = mocked_album
        self.assertEqual(edit_album(), ('Album does not exists!', 404))

        mocked_album.count.return_value = 2
        self.assertEqual(
            edit_album(), ('Cannot delete album, error with ID!', 404))

        mocked_album.count.return_value = 1
        mock_request.form['album_name'] = 'test name'
        mock_request.form['album_description'] = 'test description'
        self.assertEqual(edit_album(), ('', 200))

        del mock_db
        del mock_app


if __name__ == '__main__':
    unittest.main()
