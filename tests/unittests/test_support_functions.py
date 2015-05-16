"""Tests for various support functions."""

import unittest

from sqlalchemy.orm.exc import ObjectDeletedError
from unittest.mock import patch
from unittest.mock import MagicMock

from pagapp.support_functions import load_user, flash_form_errors


class LoadUserTestCase(unittest.TestCase):
    """Tests for load_user() function."""

    @patch('pagapp.support_functions.Users')
    def test_load_user(self, mock_users):
        """Test for load_user() function.

        Test case:
        Function should return Users.query.get() result if it do not
        raises ObjectDeletedError.
        """
        test_value = 'test1233321'
        mock_users.query.get.return_value = test_value
        self.assertEqual(load_user(1), test_value)

    @patch('pagapp.support_functions.Users')
    def test_load_user(self, mock_users):
        """Test for load_user() function.

        Test case:
        If Users.query.get() raises ObjectDeletedError - function should
        return None.
        """
        test_value = 'test1233321'
        mock_state = MagicMock()
        mock_state.class_.return_value = None
        mock_state.class_.__name__ = test_value
        mock_state.obj.return_value = None
        mock_users.query.get.side_effect = ObjectDeletedError(
            state=mock_state)
        self.assertEqual(load_user(1), None)


class FlashFormErrorsTestCase(unittest.TestCase):
    """Tests for flash_form_errors() function."""

    @patch('pagapp.support_functions.flash')
    def test_flash_form_errors(self, mock_flash):
        """Test for flash_form_errors() function.

        Test cases:
        Function should raise flash() for every error from errors array,
        for every errors array assigned with field.
        """
        mock_form = MagicMock()
        mock_form.errors.items.return_value = \
            [('field1', ['error1', 'error2', 'error3']),
             ('field2', ['error4', 'error5', 'error6']),
             ('field3', ['error7', 'error8', 'error9'])]
        flash_form_errors(mock_form)
        self.assertTrue(mock_flash.called, msg="flash() should be called!")


if __name__ == '__main__':
    unittest.main()
