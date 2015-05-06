"""Tests description of "pictures" table in database."""

import datetime
import unittest

from pagapp.models.pictures import Pictures


class PicturesTableTestCase(unittest.TestCase):
    """Test for pagapp.models.Pictures class, which describes DB table.

    Test case:
    test_service_methods -- tests Pictures constructor and __repr__
    function.
    """

    def test_service_methods(self):
        """Test for Pictures constructor and __repr__ function

        Test cases:
        All constructor's parameters is ok.
        Return value of __repr__() function should contain parameters,
        given to constructor.
        If name parameter is omitted - empty string should be used.
        Constructor should raise TypeError exception if one or more
        parameters are not strings.
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

        repr_result = test_picture.__repr__()
        expected_repr_result = \
            'Album ID: {}, Uploader ID: {}, Date: {}, Path: {}|{}, ' \
            'Name: {}'.format(1, 2,
                              datetime.datetime(2009, 1, 2, 12, 14, 22, 34),
                              'fake_path', 'fake_path_thumbnail', '')
        self.assertEqual(repr_result, expected_repr_result)

        wrong_arguments_array = \
            [{'album_id': 'error',
              'uploader_id': 2,
              'upload_date': datetime.datetime.now(),
              'path_to_image': 'path',
              'path_to_thumbnail': 'path',
              'name': 'name'},
             {'album_id': 1,
              'uploader_id': 'error',
              'upload_date': datetime.datetime.now(),
              'path_to_image': 'path',
              'path_to_thumbnail': 'path',
              'name': 'name'},
             {'album_id': 1,
              'uploader_id': 2,
              'upload_date': 'error',
              'path_to_image': 'path',
              'path_to_thumbnail': 'path',
              'name': 'name'},
             {'album_id': 1,
              'uploader_id': 2,
              'upload_date': datetime.datetime.now(),
              'path_to_image': 1,
              'path_to_thumbnail': 'path',
              'name': 'name'},
             {'album_id': 1,
              'uploader_id': 2,
              'upload_date': datetime.datetime.now(),
              'path_to_image': 'path',
              'path_to_thumbnail': 1,
              'name': 'name'},
             {'album_id': 1,
              'uploader_id': 2,
              'upload_date': datetime.datetime.now(),
              'path_to_image': 'path',
              'path_to_thumbnail': 'path',
              'name': 1}
             ]
        for wrong_arguments in wrong_arguments_array:
            self.assertRaises(TypeError, Pictures.__init__,
                              wrong_arguments,
                              msg="TypeError raises if argument(s) wrong!")


if __name__ == '__main__':
    unittest.main()
