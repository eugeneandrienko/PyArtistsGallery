"""Tests description of "pictures" table in database."""

import datetime
import unittest

from pagapp.models.pictures import Pictures


class PicturesTableTestCase(unittest.TestCase):
    """Test for pagapp.models.Pictures class, which describes DB table.

    Test cases:
    test_service_methods -- tests Pictures constructor and __repr__
    function.
    test_wrong_parameters -- tests Pictures constructor with wrong
    arguments.
    """

    def test_service_methods(self):
        """Test for Pictures constructor and __repr__ function

        Test cases:
        All constructor's parameters is ok.
        Return value of __repr__() function should contain parameters,
        given to constructor.
        If name parameter is omitted - empty string should be used.
        """
        test_arguments = {
            'album_id': 1,
            'uploader_id': 2,
            'upload_date': datetime.datetime(2009, 1, 2, 12, 14, 22, 34),
            'path_to_image': 'fake_path',
            'path_to_thumbnail': 'fake_path_thumbnail',
            'name': 'fake name'
        }
        test_picture = Pictures(test_arguments)
        self.assertEqual(
            {
                'album_id': test_picture.album_id,
                'uploader_id': test_picture.uploader_id,
                'upload_date': test_picture.upload_date,
                'path_to_image': test_picture.path_to_image,
                'path_to_thumbnail': test_picture.path_to_thumbnail,
                'name': test_picture.name
            },
            test_arguments,
            msg="Album ID, date and etc should be equal!")

        test_arguments = {
            'album_id': 1,
            'uploader_id': 2,
            'upload_date': datetime.datetime(2009, 1, 2, 12, 14, 22, 34),
            'path_to_image': 'fake_path',
            'path_to_thumbnail': 'fake_path_thumbnail',
            'name': ''
        }
        test_picture = Pictures(test_arguments)
        repr_result = test_picture.__repr__()
        expected_repr_result = \
            'Album ID: {}, Uploader ID: {}, Date: {}, Path: {}|{}, ' \
            'Name: {}'.format(1, 2,
                              datetime.datetime(2009, 1, 2, 12, 14, 22, 34),
                              'fake_path', 'fake_path_thumbnail', '')
        self.assertEqual(repr_result, expected_repr_result)

    def test_wrong_parameters(self):
        """Test for Pictures constructor.

        Test case:
        Constructor should raise TypeError exception if one or more
        parameters are not strings.
        """
        wrong_arguments_array = \
            [('error', 2, datetime.datetime.now(), 'path', 'path', 'name'),
             (1, 'error', datetime.datetime.now(), 'path', 'path', 'name'),
             (1, 2, 'error', 'path', 'path', 'name'),
             (1, 2, datetime.datetime.now(), 1, 'path', 'name'),
             (1, 2, datetime.datetime.now(), 'path', 1, 'name'),
             (1, 2, datetime.datetime.now(), 'path', 'path', 1)]
        arguments_keys = ('album_id', 'uploader_id', 'upload_date',
                          'path_to_image', 'path_to_thumbnail', 'name')
        for wrong_arguments in wrong_arguments_array:
            self.assertRaises(
                TypeError, Pictures.__init__,
                {key: value for key, value in zip(arguments_keys,
                                                  wrong_arguments)},
                msg="TypeError raises if argument(s) wrong!")


if __name__ == '__main__':
    unittest.main()
