"""Tests for module, within pagapp creates."""

from logging import ERROR
import unittest
from unittest.mock import patch
from unittest.mock import MagicMock

from pagapp.create_pagapp import create_pagapp, register_blueprints, \
    setup_logging, check_folders


class CreatePagappTestCase(unittest.TestCase):
    """Test for function, which create pagapp application.

    Test case:
    test_create_pagapp() - tests for create_pagapp().
    """

    @patch('pagapp.create_pagapp.db')
    @patch('pagapp.create_pagapp.lm')
    @patch('pagapp.create_pagapp.Flask')
    def test_create_pagapp(self, mock_flask, mock_lm, mock_db):
        """Test for create_pagapp() function.

        Test cases:
        Inside this function we should call bunch of flask function and
        return app value, which previously returned by Flask() function
        within.
        And assume, what directory to uploads already exists.
        """
        path_to_config = 'path_to_config'
        mock_app = MagicMock()
        mock_app.config['STATIC_FOLDER'] = 'static folder'
        mock_app.config['TEMPLATES_FOLDER'] = 'templates folder'
        mock_lm.init_app.return_value = None
        mock_db.init_app.return_value = None

        mock_flask.return_value = mock_app

        path_to_register_blueprints = 'pagapp.create_pagapp.register_blueprints'
        path_to_setup_logging = 'pagapp.create_pagapp.setup_logging'
        path_to_check_folders = 'pagapp.create_pagapp.check_folders'
        with patch(path_to_register_blueprints) as mock_register_blueprints, \
                patch(path_to_setup_logging) as mock_setup_logging, \
                patch(path_to_check_folders) as mock_check_folders:
            self.assertEqual(create_pagapp(path_to_config, debug=True),
                             mock_app, msg="create_pagapp() called successfully")
            mock_app.config.from_object.assert_called_with(path_to_config)
            self.assertTrue(mock_register_blueprints.called)
            self.assertTrue(mock_setup_logging.called)
            self.assertTrue(mock_check_folders.called)
            self.assertTrue(mock_app.logger.info.called)


class RegisterBlueprintsTestCase(unittest.TestCase):
    """Test for register_blueprints()."""

    def test_register_blueprints(self):
        """Test for register_blueprints().

        Test case:
        app.register_blueprint(...) should be called in all cases.
        """
        mock_app = MagicMock()
        register_blueprints(mock_app)
        self.assertTrue(mock_app.register_blueprint)


class SetupLoggingTestCase(unittest.TestCase):
    """Test for setup_logging()."""

    @patch('pagapp.create_pagapp.RotatingFileHandler')
    def test_setup_logging(self, mock_rotating_file_handler):
        """Test for setup_logging().

        Test cases:
        If application not in debugging state we should use RotatingFileHandler().
        """
        mock_handler = MagicMock()
        mock_app = MagicMock()

        mock_app.debug = False
        mock_rotating_file_handler.return_value = mock_handler
        setup_logging(mock_app)
        mock_handler.setLevel.assert_called_with(ERROR)


class CheckFoldersTestCase(unittest.TestCase):
    """Tests for check_folders() function."""

    @patch('pagapp.create_pagapp.exists')
    @patch('pagapp.create_pagapp.dirname')
    def test_check_folders_exists(self, mock_dirname, mock_exists):
        """Test for check_folders().

        Test case:
        If all folders exists - function should
        just write to log about it.
        """
        mock_exists.return_value = True
        mock_app = MagicMock()
        check_folders(mock_app)
        self.assertTrue(mock_app.logger.info.called)
        del mock_dirname

    @patch('pagapp.create_pagapp.makedirs')
    @patch('pagapp.create_pagapp.exists')
    @patch('pagapp.create_pagapp.dirname')
    def test_check_folders_not_exists(self, mock_dirname, mock_exists,
                                      mock_makedirs):
        """Test for check_folders().

        Test case:
        If folders do not exists - function should wirte
        about it to log and create non-existent directory.
        """
        mock_exists.return_value = False
        mock_app = MagicMock()
        check_folders(mock_app)
        self.assertTrue(mock_app.logger.error.called)
        self.assertTrue(mock_makedirs.called)
        del mock_dirname


if __name__ == '__main__':
    unittest.main()
