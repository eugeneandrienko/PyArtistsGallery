"""Tests for forms from pagapp.forms.pictures"""

import unittest

from pagapp.forms import PictureForm
from unittest import mock


class PictureFormTestCase(unittest.TestCase):
    """Tests for form PictureForm.

    Test cases:
    Method should call filter_by() with given album_id parameter.
    """

    @mock.patch('pagapp.forms.pictures.Pictures.query')
    def test_get_pictures(self, mock_query):
        """Test for get_pictures() method.

        Test cases:
        """
        test_album_id = 123
        test_picture_form = PictureForm()
        test_picture_form.get_pictures(test_album_id)
        self.assertTrue(mock_query.filter_by.called,
                        msg="filter_by should be called!")
        mock_query.filter_by.assert_called_with(album_id=test_album_id)


if __name__ == '__main__':
    unittest.main()
