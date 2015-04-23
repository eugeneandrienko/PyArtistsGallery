"""Tests for forms from pagapp.forms.albums."""

import unittest
from unittest import mock

from pagapp.forms import AlbumForm


class AlbumFormTestCase(unittest.TestCase):
    """Test for AlbumForm form.

    Test cases:
    test_init -- tests __init__() function.
    test_get_albums_list -- tests function, which should return all albums
    from database.
    """

    class MockFilterByReturnValue():
        """Special mock object for filter_by() function.

        filter_by() function returns object with first() method.
        We use this method inside code of our application.
        """

        @staticmethod
        def first():
            """Special method, which uses inside code of out application."""
            return 'test value'

    @mock.patch('pagapp.models.Albums.query')
    def test_init(self, mock_query):
        """Tests __init__() function.

        Test cases:
        If we do not pass any arguments to constructor - matched_album
        field should be equal with None.
        If we pass URL to constructor -- we should call corresponding
        branch of code inside the constructor and initialize matched_album
        field.
        """
        test_album = AlbumForm()
        self.assertEqual(test_album.matched_album, None,
                         msg="matched_album should be None!")
        self.assertFalse(mock_query.filter_by.called,
                         msg="filter_by() should not be called!")

        mock_query.filter_by.return_value = self.MockFilterByReturnValue()
        test_parameter = 'Test321'
        test_album = AlbumForm(test_parameter)
        self.assertNotEqual(test_album.matched_album, None,
                            msg="matched_album should not be None!")
        self.assertTrue(mock_query.filter_by.called,
                        msg="filter_by should be called!")
        mock_query.filter_by.assert_called_with(url_part=test_parameter)

    @mock.patch('pagapp.models.Albums.get_albums_list')
    def test_get_albums_list(self, mock_get_albums_list):
        """Tests get_albums_list() function.

        Test case:
        This method should call get_albums_list() function.
        """
        test_album = AlbumForm()
        test_album.get_albums_list()
        self.assertTrue(mock_get_albums_list.called,
                        msg="get_albums_list() should be called!")


if __name__ == '__main__':
    unittest.main()