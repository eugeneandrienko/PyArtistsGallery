"""Test for index() function from views."""

import unittest

from unittest import mock

from pagapp.views.main import index


class MainPyTestCase(unittest.TestCase):
    """Test for pagapp.views.main module.

     Test cases:
     test_index(): tests index() function.
     """

    @mock.patch('pagapp.views.main.render_template')
    @mock.patch('pagapp.views.main.url_for')
    @mock.patch('pagapp.views.main.redirect')
    @mock.patch('pagapp.views.main.GotoUploadFakeForm')
    def test_index(self, mock_fake_form, mock_redirect, mock_url_for,
                   mock_render_template):
        """Test for index() function.

        Test cases:
        If user press submit button on the GotoUploadFakeForm - function
        should redirect us to upload page.
        In all other cases function should return rendered template for
        the main site page.
        """
        redirect_result = 'redirect'
        render_template_result = 'render_template'

        mock_fake_form.return_value.validate_on_submit.return_value = True
        mock_url_for.return_value = 'test'
        mock_redirect.return_value = redirect_result
        self.assertEqual(index(), redirect_result,
                         msg="redirect() should be called!")

        mock_fake_form.return_value.validate_on_submit.return_value = False
        mock_render_template.return_value = render_template_result
        self.assertEqual(index(), render_template_result,
                         msg="render_template() should be called!")


if __name__ == '__main__':
    unittest.main()
