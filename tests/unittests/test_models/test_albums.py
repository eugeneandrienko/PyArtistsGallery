"""Tests description of "albums" table in database."""

import unittest

from unittest.mock import patch

from pagapp.models.albums import Albums


class AlbumsTableTestCase(unittest.TestCase):
    """Test for pagapp.models.Albums class, which describes DB table.

    Test cases:
    test_service_methods -- tests Albums constructor and __repr__ function,
    which uses for debug purposes.
    test_get_albums_list -- tests function, which returns list of all albums.
    """

    def test_service_methods(self):
        """Test for Albums constructor and __repr__ function.

        Test cases:
        All constructor's parameters is ok.
        Return value of __repr__() function should contain parameters,
        given to constructor.
        Constructor should raise TypeError exception if one or more
        parameters are not strings.
        """
        test_arguments = ('www.example.com', 'Test Album Name',
                          'Test Album Description')
        test_album = Albums(*test_arguments)
        self.assertTupleEqual(
            (test_album.url_part,
             test_album.album_name,
             test_album.album_description),
            test_arguments,
            msg="URL, name and description should be equal!")

        repr_result = test_album.__repr__()
        expected_repr_result = \
            'URL part: {}, Album: {}, Description: {}'.format(*test_arguments)
        self.assertEqual(repr_result, expected_repr_result)

        wrong_arguments_array = [(1, 'Name', 'Description'),
                                 ('URL', 1, 'Description'),
                                 ('URL', 'Name', 1)]
        for wrong_arguments in wrong_arguments_array:
            self.assertRaises(TypeError,
                              Albums.__init__,
                              *wrong_arguments,
                              msg="TypeError raises if argument(s) wrong!")

    @patch('pagapp.models.albums.Albums')
    def test_get_albums_list(self, mock_albums):
        """Tests method, which should return list of all albums.

        Test cases:
        There are no albums in the database.
        There is(are) something album(s) in the database.
        """
        test_album = Albums('fake_url', 'fake_name', 'fake')

        mock_albums.query.all.return_value = []
        result = test_album.get_albums_list()
        self.assertEqual(result, [], msg="Albums list should be empty.")

        mock_albums.query.all.return_value = [test_album]
        result = test_album.get_albums_list()
        self.assertEqual(result,
                         [{'url_part': 'fake_url',
                           'album_name': 'fake_name',
                           'album_description': 'fake'}])


if __name__ == '__main__':
    unittest.main()
