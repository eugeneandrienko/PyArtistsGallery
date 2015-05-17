"""Tests for module, within pagapp creates."""

import unittest
from unittest.mock import patch
from unittest.mock import MagicMock

from pagapp.create_pagapp import create_pagapp


class CreatePagappTestCase(unittest.TestCase):
    """Tests for function, which create pagapp application.

    Test cases:
    test_create_pagapp() - tests for create_pagapp() function.
    """

    @patch('pagapp.create_pagapp.db')
    @patch('pagapp.create_pagapp.lm')
    @patch('pagapp.create_pagapp.Flask')
    def test_create_pagapp(self, mock_flask, mock_lm, mock_db):
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
        mock_app.register_blueprint.return_value = None
        mock_app.register_blueprint.return_value = None

        mock_flask.return_value = mock_app

        self.assertEqual(create_pagapp(path_to_config=path_to_config),
                         mock_app, msg="create_pagapp() called successfully")
        mock_app.config.from_object.assert_called_with(path_to_config)


if __name__ == '__main__':
    unittest.main()
