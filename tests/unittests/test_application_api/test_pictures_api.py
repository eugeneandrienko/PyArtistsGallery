"""Tests for pictures' API calls."""

from flask_login import login_user
import json
import datetime
import unittest
from unittest.mock import patch
from unittest.mock import MagicMock

from pagapp.models.users import Users
from pagapp.application_api.pictures_api import get_pictures_list
from pagapp.application_api.pictures_api import delete_picture, edit_picture
from tests.unittests.flask_test import FlaskApplicationContextTestCase


class GetPicturesListTestCase(FlaskApplicationContextTestCase):
    """Tests for /api/get-pictures-list API calls."""

    @patch('pagapp.application_api.pictures_api.request')
    @patch('pagapp.application_api.pictures_api._generate_picture_table_item')
    @patch('pagapp.application_api.pictures_api.Pictures')
    def test_get_pictures_list(self, mock_pictures,
                               mock_generate_picture_table_item, mock_request):
        """Test for /api/get-pictures-list API call.

        Test case:
        In every case we should return json with list
        of pictures.
        """
        login_user(Users('nickname', 'password', True))
        mock_request.json = {'album_id': 1}

        mock_picture = MagicMock()
        mock_picture.name = 'test_name'
        mock_picture.description = 'test description'
        mock_picture.id = 1
        mock_picture.path_to_thumbnail = '/path'
        mock_picture.upload_date = datetime.datetime.utcnow()

        mock_pictures.query.filter_by.return_value.count.return_value = 1
        mock_generate_picture_table_item.return_value = {'test1': 'test2'}

        mock_pictures.query.filter_by.return_value.all.return_value = \
            [mock_picture]

        expected_result = json.dumps(
            [
                {
                    'test1': 'test2'
                }
            ]
        )

        self.assertEqual(get_pictures_list(), expected_result)


class DeletePictureTestCase(FlaskApplicationContextTestCase):
    """Tests for delete_picture() function."""

    @patch('pagapp.application_api.pictures_api.current_app')
    @patch('pagapp.application_api.pictures_api.request')
    @patch('pagapp.application_api.pictures_api.Pictures')
    def test_delete_album(self, mock_pictures, mock_request, mock_app):
        """Test for /delete-picture API call.

        Test cases:
        If count of pictures with given id is not equal with one - function
        should return tuple ('some text', 404).
        Else, if count of albums equals with one - function should
        return tuple ('', 200).
        """
        login_user(Users('nickname', 'password', True))

        mock_picture = MagicMock()
        mock_picture.first.return_value = 'test'
        mock_picture.count.return_value = 2
        mock_pictures.query.filter_by.return_value = mock_picture
        self.assertEqual(delete_picture(), (
            'Cannot delete picture, too much IDs!', 404))

        with patch('pagapp.application_api.pictures_api.db') as mock_db:
            mock_picture.count.return_value = 1
            mock_pictures.query.filter_by.return_value = mock_picture
            self.assertEqual(delete_picture(), ('', 200))
            del mock_db
        del mock_request
        del mock_app


class EditPictureTestCase(FlaskApplicationContextTestCase):
    """Tests for /api/edit-picture API call."""

    @patch('pagapp.application_api.pictures_api.current_app')
    @patch('pagapp.application_api.pictures_api.db')
    @patch('pagapp.application_api.pictures_api.request')
    @patch('pagapp.application_api.pictures_api.Pictures')
    def test_edit_album(self, mock_pictures, mock_request, mock_db, mock_app):
        """Test for edit_picture() function.

        Test cases:
        If count of pictures with given ID is not equal with one - function
        should return 404 error.
        Otherwise it should rename picture and return code 200.
        """
        login_user(Users('nickname', 'password', True))
        mocked_picture = MagicMock()

        mocked_picture.count.return_value = 0
        mock_pictures.query.filter_by.return_value = mocked_picture
        self.assertEqual(edit_picture(), ('Picture does not exists!', 404))

        mocked_picture.count.return_value = 2
        self.assertEqual(
            edit_picture(), ('Cannot edit picture, too much IDs!', 404))

        mocked_picture.count.return_value = 1
        mock_request.form['picture_name'] = 'test name'
        mock_request.form['picture_description'] = 'test description'
        self.assertEqual(edit_picture(), ('', 200))

        del mock_db
        del mock_app


if __name__ == '__main__':
    unittest.main()
