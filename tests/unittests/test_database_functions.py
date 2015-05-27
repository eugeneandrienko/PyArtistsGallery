"""Tests for different database functions."""

import unittest
from unittest.mock import patch

from pagapp.database_functions import create_database, upgrade_database
from tests.unittests.flask_test import FlaskApplicationContextTestCase


class CreateDatabaseTestCase(FlaskApplicationContextTestCase):
    """Tests for create_database() function."""

    @patch('pagapp.database_functions.db')
    def test_create_database(self, mock_db):
        """Test for create_database() function.

        Test case:
        In all cases this function should call db.create_all(),
        create 'alembic_version' table with all needed data and exit.
        """
        with patch('pagapp.database_functions.current_app') as mock_app:
            mocked_version = '1.0test_mock'
            mock_app.config['SQLALCHEMY_DATABASE_VERSION'] = mocked_version
            create_database()
            self.assertTrue(mock_db.create_all.called)
            self.assertTrue(mock_db.session.add.called)


class UpgradeDatabaseTestCase(FlaskApplicationContextTestCase):
    """Tests for upgrade_database() functuion."""

    @patch('pagapp.database_functions.current_app')
    @patch('pagapp.database_functions.upgrade')
    def test_upgrade_database(self, mock_upgrade, mock_app):
        """Test for upgrade_database() function.

        Test case:
        In all cases function should call upgrade()
        function.
        """
        upgrade_database()
        self.assertTrue(mock_upgrade.called)
        del mock_app


if __name__ == '__main__':
    unittest.main()
