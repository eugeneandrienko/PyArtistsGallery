"""Test for views from admin panel."""

import unittest

from jinja2 import TemplateNotFound
from unittest.mock import patch
from flask_login import login_user

from pagapp.models.users import Users
from pagapp.admin_panel.views import logout, panel
from tests.unittests.flask_test import FlaskApplicationContextTestCase


class AdminPanelViewsTestCase(FlaskApplicationContextTestCase):
    """Tests for functions from admin panel's views.

    Test cases:
    test_logout() - tests for logout() function.
    test_panel() - tests for panel() function.
    """

    @patch('pagapp.admin_panel.views.url_for')
    @patch('pagapp.admin_panel.views.redirect')
    @patch('pagapp.admin_panel.views.logout_user')
    def test_logout(self, mock_logout_user, mock_redirect, mock_url_for):
        """Tests for logout() function.

        Test cases:
        Function should call logout_user() and redirect()
        functions in any cases.
        """
        redirect_result = 'redirect() test'
        mock_url_for.return_value = 'test'
        mock_redirect.return_value = redirect_result
        login_user(Users('nickname', 'password', 'salt', True))
        self.assertEqual(logout(), redirect_result,
                         msg="redirect() should be called!")
        self.assertTrue(mock_url_for.called)
        self.assertTrue(mock_logout_user.called)

    @patch('pagapp.admin_panel.views.abort')
    @patch('pagapp.admin_panel.views.current_app')
    @patch('pagapp.admin_panel.views.render_template')
    def test_panel(self, mock_render_template, mock_current_app, mock_abort):
        """Tests for panel() function.

        Test cases:
        Function should call render_template() except if template does
        not found - then we should call abort(404).
        In all cases we should call all form controllers.
        """
        login_user(Users('nickname', 'password', 'salt', True))
        render_template_result = 'render_template() result'
        mock_render_template.return_value = render_template_result
        mock_current_app.config['GALLERY_TITLE'] = 'test'
        self.assertEqual(panel(), render_template_result,
                         msg="render_template() should be called!")

        with patch('pagapp.admin_panel.views.ChangePasswordForm') \
                as mock_change_password_form:
            mock_render_template.side_effect = TemplateNotFound(name='test')
            panel()
            self.assertTrue(mock_change_password_form.called)
            self.assertTrue(mock_abort.called)


if __name__ == '__main__':
    unittest.main()
