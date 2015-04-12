"""Tests description of "pictures" table in database."""

import datetime
import unittest

from pagapp.models import Pictures


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
        Constructor should raise TypeError exception if one or more
        parameters are not strings.
        """
        test_arguments = (1, 2, datetime.datetime(2009, 1, 2, 12, 14, 22, 34),
                          'fake path', 'fake_path_thumbnail', 'fake name')
        test_picture = Pictures(*test_arguments)
        self.assertTupleEqual((test_picture.album_id,
                               test_picture.uploader_id,
                               test_picture.upload_date,
                               test_picture.path_to_image,
                               test_picture.path_to_thumbnail,
                               test_picture.name),
                              test_arguments,
                              msg="Album ID, date and etc should be equal!")

        repr_result = test_picture.__repr__()
        expected_repr_result = \
            'Album ID: {}, Uploader ID: {}, Date: {}, Path: {}|{}, ' \
            'Name: {}'.format(*test_arguments)
        self.assertEqual(repr_result, expected_repr_result)

        wrong_arguments_array = \
            [('error', 2, datetime.datetime.now(), 'path', 'path', 'name'),
             (1, 'error', datetime.datetime.now(), 'path', 'path', 'name'),
             (1, 2, 'error', 'path', 'path', 'name'),
             (1, 2, datetime.datetime.now(), 1, 'path', 'name'),
             (1, 2, datetime.datetime.now(), 'path', 1, 'name'),
             (1, 2, datetime.datetime.now(), 'path', 'path', 1)]
        for wrong_arguments in wrong_arguments_array:
            self.assertRaises(TypeError, Pictures.__init__,
                              *wrong_arguments,
                              msg="TypeError raises if argument(s) wrong!")


if __name__ == '__main__':
    unittest.main()
