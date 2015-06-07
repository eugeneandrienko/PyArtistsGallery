"""Tests for functions, which save pictures, uploaded to the gallery."""

import unittest

from unittest.mock import patch
from unittest.mock import MagicMock

from pagapp.admin_panel.save_picture_functions import _create_thumbnail, \
    save_file


class CreateThumbnailTestCase(unittest.TestCase):
    """Tests for _create_thumbnail() function."""

    @patch('pagapp.admin_panel.save_picture_functions.current_app')
    @patch('pagapp.admin_panel.save_picture_functions.Image')
    def test_create_thumbnail_small(self, mock_image, mock_app):
        """Test for _create thumbnail() function.

        Test case:
        If size of given image lesser than values from
        THUMBNAIL_SIZE (multiplied by 2) - function should not call
        image.thumbnail() with Image.NEAREST.
        Only image.thumbnail(..., Image.ANTIALIAS) and image.save().
        """
        mock_app.config = {'THUMBNAIL_SIZE': {'x': 10, 'y': 10}}

        mock_picture = MagicMock()
        mock_picture.size = [5, 5]

        mock_image.open.return_value = mock_picture

        _create_thumbnail('test', 'test')
        self.assertTrue(mock_picture.thumbnail.called)
        mock_picture.thumbnail.assert_called_with(
            (10, 10), mock_image.ANTIALIAS)
        self.assertTrue(mock_picture.save.called)

    @patch('pagapp.admin_panel.save_picture_functions.current_app')
    @patch('pagapp.admin_panel.save_picture_functions.Image')
    def test_create_thumbnail_large(self, mock_image, mock_app):
        """Test for _create thumbnail() function.

        Test case:
        If size of given image bigger than values from
        THUMBNAIL_SIZE (multiplied by 2) - function should call
        image.thumbnail() with Image.NEAREST. And after: image.thumbnail(...,
        Image.ANTIALIAS) and image.save().
        """
        mock_app.config = {'THUMBNAIL_SIZE': {'x': 10, 'y': 10}}

        mock_picture = MagicMock()
        mock_picture.size = [50, 50]

        mock_image.open.return_value = mock_picture

        _create_thumbnail('test', 'test')
        self.assertTrue(mock_picture.thumbnail.called)
        self.assertEqual(mock_picture.thumbnail.call_count, 2)
        self.assertTrue(mock_picture.save.called)


class SaveFileTestCase(unittest.TestCase):
    """Tests for save_file() functions."""

    @patch('pagapp.admin_panel.save_picture_functions.Pictures')
    def test_save_file_already_saved(self, mock_pictures):
        """Test for save_file().

        Test case:
        File already saved (according to the database).
        """
        path_to_secure_filename = \
            'pagapp.admin_panel.save_picture_functions.secure_filename'
        path_to_app = 'pagapp.admin_panel.save_picture_functions.current_app'
        path_to_flash = 'pagapp.admin_panel.save_picture_functions.flash'
        with patch(path_to_secure_filename) as mock_secure_filename, \
                patch(path_to_app) as mock_app, \
                patch(path_to_flash) as mock_flash:
            mock_app.config = {
                'UPLOAD_FOLDER': 'test',
                'UPLOAD_FOLDER_RELATIVE': 'test'}
            mock_secure_filename.return_value = 'test'
            mock_pictures.query.filter_by.return_value.count.return_value = 1

            mock_filename_field = MagicMock()
            mock_filename_field.data.filename = 'test'

            save_file(mock_filename_field, 1, 'test', 'test')

            self.assertTrue(mock_app.logger.info.called)
            self.assertTrue(mock_app.logger.warning.called)
            self.assertTrue(mock_flash.called)

    @patch('pagapp.admin_panel.save_picture_functions._create_thumbnail')
    @patch('pagapp.admin_panel.save_picture_functions.db')
    @patch('pagapp.admin_panel.save_picture_functions.Pictures')
    def test_save_file(self, mock_pictures, mock_db, mock_create_thumbnail):
        """Test for save_file().

        Test case:
        File not saved already (according to the database) and function
        tries to save it.
        """
        path_to_secure_filename = \
            'pagapp.admin_panel.save_picture_functions.secure_filename'
        path_to_app = 'pagapp.admin_panel.save_picture_functions.current_app'
        path_to_flash = 'pagapp.admin_panel.save_picture_functions.flash'
        path_to_current_user = \
            'pagapp.admin_panel.save_picture_functions.current_user'
        path_to_os = 'pagapp.admin_panel.save_picture_functions.os'
        with patch(path_to_secure_filename) as mock_secure_filename, \
                patch(path_to_app) as mock_app, \
                patch(path_to_flash) as mock_flash, \
                patch(path_to_current_user) as mock_current_user, \
                patch(path_to_os) as mock_os:
            mock_app.config = {
                'UPLOAD_FOLDER': 'test',
                'UPLOAD_FOLDER_RELATIVE': 'test'}
            mock_secure_filename.return_value = 'test'
            mock_pictures.query.filter_by.return_value.count.return_value = 0
            mock_current_user.id = 1

            mock_filename_field = MagicMock()
            mock_filename_field.data.filename = 'test'

            mock_os.stat.return_value.st_size = 2049

            save_file(mock_filename_field, 1, 'test', 'test')

            self.assertTrue(mock_app.logger.info.call_count, 2)
            self.assertTrue(mock_filename_field.data.save.called)
            self.assertTrue(mock_create_thumbnail.called)
            self.assertTrue(mock_pictures.called)
            self.assertTrue(mock_db.session.add.called)
            self.assertTrue(mock_db.session.commit.called)
            self.assertTrue(mock_flash.called)


if __name__ == '__main__':
    unittest.main()
