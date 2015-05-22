"""Tests for 'alembic_version' model."""

import unittest

from pagapp.models.alembic_version import AlembicVersion


class AlembicVersionTableTestCase(unittest.TestCase):
    """Tests for 'pagapp.models.alembic_version' class.

    Test cases:
    test_init() -- tests __init__() function.
    test_repr() -- tests __repr__() function.
    """

    def test_init(self):
        """Test for __init__() function.

        Test cases:
        Given parameter should pass to class' field.
        If parameter is not a string - we should get an exception.
        """
        test_argument = 'test_version123'
        test_alembic_version = AlembicVersion(test_argument)
        self.assertEqual(
            test_alembic_version.version_num,
            test_argument)

        test_argument = 123
        self.assertRaises(TypeError,
                          AlembicVersion.__init__,
                          test_argument)

    def test_repr(self):
        """Test for __repr__() function."""
        test_argument = 'test_version123'
        test_alembic_version = AlembicVersion(test_argument)
        expected_result = 'Version: {}'.format(test_argument)
        self.assertEqual(
            test_alembic_version.__repr__(),
            expected_result)


if __name__ == '__main__':
    unittest.main()
