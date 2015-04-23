"""Tests description of "albums" table in database."""

import unittest
from unittest import mock

from pagapp.models import Albums

# For test_get_albums_list() method.
COUNT_OF_FAKE_ALBUMS = 5


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

    @mock.patch('pagapp.models.Albums.query')
    def test_get_albums_list(self, mock_query):
        """Tests method, which should return list of all albums.

        Test cases:
        There are no albums in the database.
        There is(are) something album(s) in the database.
        """
        test_album = Albums('fake_url', 'fake_name', 'fake')
        mock_query.all.return_value = []
        result = test_album.get_albums_list()
        self.assertEqual(result, [], msg="Albums list should be empty.")

        expected_value = []
        all_return_value = []
        for index, elements_in_database in enumerate(range(
                COUNT_OF_FAKE_ALBUMS)):
            expected_value.append(
                {'url_part': 'test_url' + str(elements_in_database),
                 'album_name': 'test_album_name' + str(elements_in_database),
                 'album_description': 'test_album_description' + str(
                     elements_in_database)})

            mock_album = mock.create_autospec(Albums)
            (mock_album.url_part,
             mock_album.album_name,
             mock_album.album_description) = (expected_value[index]['url_part'],
                                              expected_value[index][
                                                  'album_name'],
                                              expected_value[index][
                                                  'album_description'])
            all_return_value.append(mock_album)
            mock_query.all.return_value = all_return_value

            result = test_album.get_albums_list()
            self.assertEqual(result, expected_value,
                             msg="There is should be {} album(s)".format(
                                 elements_in_database))


if __name__ == '__main__':
    unittest.main()