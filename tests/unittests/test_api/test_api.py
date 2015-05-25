"""Tests for API calls."""

from flask_login import login_user
import json
import unittest
from unittest.mock import patch
from unittest.mock import MagicMock

from pagapp.models.users import Users
from pagapp.application_api.api import get_albums_list, delete_album
from tests.unittests.flask_test import FlaskApplicationContextTestCase


class GetAlbumsListTestCase(unittest.TestCase):
    """Tests for /api/get-albums-list API call."""

    @patch('pagapp.application_api.api.Pictures')
    @patch('pagapp.application_api.api.Albums')
    def test_get_albums_list(self, mock_albums, mock_pictures):
        """Test for /api/get-album-list API call.

        Test case:
        In every case we should return json with list
        of albums.
        """
        mock_album = MagicMock()
        mock_album.album_name = 'test_name'
        mock_album.album_description = 'test description'
        mock_album.id = 1

        mock_pictures.query.filter_by.return_value.count.return_value = 1

        mock_albums.query.all.return_value = [mock_album]

        expected_result = json.dumps(
            [
                {
                    'name': 'test_name',
                    'pics_count': 1,
                    'description': 'test description',
                    'delete': u'<button class="btn btn-danger" ' +
                              'onclick="deleteAlbum(1)">Delete album</button>'
                }
            ]
        )

        self.assertEqual(get_albums_list(), expected_result)


class DeleteAlbumTestCase(FlaskApplicationContextTestCase):
    """Tests for delete_album() function."""

    @patch('pagapp.application_api.api.request')
    @patch('pagapp.application_api.api.Albums')
    def test_delete_album(self, mock_albums, mock_request):
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

        with patch('pagapp.application_api.api.db') as mock_db:
            mock_album.count.return_value = 1
            mock_albums.query.filter_by.return_value = mock_album
            self.assertEqual(delete_album(), ('', 200))
            del mock_db
        del mock_request


if __name__ == '__main__':
    unittest.main()
