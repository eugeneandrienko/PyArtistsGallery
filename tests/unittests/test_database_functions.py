"""Tests for different database functions."""

import unittest
from unittest.mock import patch

from pagapp.database_functions import create_database


class CreateDatabaseTestCase(unittest.TestCase):
    """Tests for create_database() function."""

    @patch('pagapp.database_functions.db')
    def test_create_database(self, mock_db):
        """Test for create_database() function.

        Test case:
        In all cases this function should call db.create_all()
        and exit.
        """
        create_database()
        self.assertTrue(mock_db.create_all.called)


if __name__ == '__main__':
    unittest.main()
