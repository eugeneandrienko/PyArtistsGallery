"""Tests for module, within pagapp creates."""

from logging import ERROR
import unittest
from unittest.mock import patch
from unittest.mock import MagicMock

from pagapp.create_pagapp import create_pagapp, register_blueprints, \
    setup_logging


class CreatePagappTestCase(unittest.TestCase):
    """Tests for function, which create pagapp application.

    Test cases:
    test_create_pagapp() - tests for create_pagapp() function.
    """

    @patch('pagapp.create_pagapp.setup_logging')
    @patch('pagapp.create_pagapp.register_blueprints')
    @patch('pagapp.create_pagapp.db')
    @patch('pagapp.create_pagapp.lm')
    @patch('pagapp.create_pagapp.Flask')
    def test_create_pagapp(self, mock_flask, mock_lm, mock_db,
                           mock_register_blueprints, mock_setup_logging):
        """Tests for create_pagapp() function.

        Test case:
        Inside this function we should call bunch of flask function and
        return app value, which previously returned by Flask() function
        within.
        """
        path_to_config = 'path_to_config'
        mock_app = MagicMock()
        mock_app.config['STATIC_FOLDER'] = 'static folder'
        mock_app.config['TEMPLATES_FOLDER'] = 'templates folder'
        mock_lm.init_app.return_value = None
        mock_db.init_app.return_value = None

        mock_flask.return_value = mock_app

        self.assertEqual(create_pagapp(path_to_config, debug=True),
                         mock_app, msg="create_pagapp() called successfully")
        mock_app.config.from_object.assert_called_with(path_to_config)
        self.assertTrue(mock_register_blueprints.called)
        self.assertTrue(mock_setup_logging.called)

    def test_register_blueprints(self):
        """Test for register_blueprints().

        Test case:
        app.register_blueprint(...) should be called in all cases.
        """
        mock_app = MagicMock()
        register_blueprints(mock_app)
        self.assertTrue(mock_app.register_blueprint)

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


if __name__ == '__main__':
    unittest.main()
