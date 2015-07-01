"""Tests for views for public pages."""

import unittest
from unittest.mock import patch
from unittest.mock import MagicMock

from jinja2 import TemplateNotFound

from pagapp.public_pages.views import index, album, login


class IndexTestCase(unittest.TestCase):
    """Tests for index() function."""

    @patch('pagapp.public_pages.views.render_template')
    def test_index(self, mock_render_template):
        """Test for index() function.

        Test case:
        We should return result of render_template() call if
        render_template() did not returns any exception.
        """
        path_to_configuration = 'pagapp.public_pages.views.Configuration'
        path_to_albums = 'pagapp.public_pages.views.Albums'
        path_first_run = 'pagapp.public_pages.views.is_first_run'
        path_is_upgrade_ready = 'pagapp.public_pages.views.is_upgrade_ready'
        with patch(path_to_configuration) as mock_configuration, \
                patch(path_to_albums) as mock_albums, \
                patch(path_first_run) as mock_first_run, \
                patch(path_is_upgrade_ready) as mock_is_upgrade_ready:
            mock_first_result = MagicMock()
            mock_first_result.gallery_title = 'test'
            mock_configuration.query.first.return_value = mock_first_result
            test_render_template = 'render_template'
            mock_render_template.return_value = test_render_template
            mock_albums.get_albums_list.return_value = 'test'
            mock_first_run.return_value = False
            mock_is_upgrade_ready.return_value = False
            self.assertEqual(index(), test_render_template,
                             msg="render_template() should be called!")

    @patch('pagapp.public_pages.views.current_app')
    @patch('pagapp.public_pages.views.abort')
    @patch('pagapp.public_pages.views.render_template')
    def test_index_no_template(self, mock_render_template, mock_abort,
                               mock_app):
        """Test for index() function.

        Test case:
        If render_template() raise TemplateNotFound - function
        should call abort(404) function.
        """
        test_abort = 'test_abort'
        mock_abort.return_value = test_abort
        mock_render_template.side_effect = TemplateNotFound(name='test')
        path_to_configuration = 'pagapp.public_pages.views.Configuration'
        path_to_albums = 'pagapp.public_pages.views.Albums'
        path_to_first_run = 'pagapp.public_pages.views.is_first_run'
        path_is_upgrade_ready = 'pagapp.public_pages.views.is_upgrade_ready'
        with patch(path_to_albums) as mock_albums, \
                patch(path_to_configuration) as mock_configuration, \
                patch(path_to_first_run) as mock_first_run, \
                patch(path_is_upgrade_ready) as mock_is_upgrade_ready:
            mock_first_result = MagicMock()
            mock_first_result.gallery_title = 'test'
            mock_configuration.query.first.return_value = mock_first_result
            mock_albums.get_albums_list.return_value = 'test'
            mock_first_run.return_value = False
            mock_is_upgrade_ready.return_value = False
            index()
            self.assertTrue(mock_abort.called,
                            msg="abort(404) should be called!")
        del mock_app

    def test_index_first_run(self):
        """Test for index() function.

        Test case:
        Function should make redirect to corresponding service page
        if it is first run of function.
        """
        path_to_first_run = 'pagapp.public_pages.views.is_first_run'
        path_to_app = 'pagapp.public_pages.views.current_app'
        path_to_url_for = 'pagapp.public_pages.views.url_for'
        path_to_redirect = 'pagapp.public_pages.views.redirect'
        with patch(path_to_first_run) as mock_first_run, \
                patch(path_to_app) as mock_app, \
                patch(path_to_url_for) as mock_url_for, \
                patch(path_to_redirect) as mock_redirect:
            mock_first_run.return_value = True
            index()
            self.assertTrue(mock_app.logger.info.called)
            self.assertTrue(mock_url_for.called)
            self.assertTrue(mock_redirect.called)

    @patch('pagapp.public_pages.views.Configuration')
    @patch('pagapp.public_pages.views.Albums')
    def test_index_update_db(self, mock_configuration, mock_albums):
        """Test for index() function.

        Test case:
        Function should perform database update if it is ready.
        """
        path_to_first_run = 'pagapp.public_pages.views.is_first_run'
        path_to_upgrade_database = 'pagapp.public_pages.views.upgrade_database'
        path_to_render_template = 'pagapp.public_pages.views.render_template'
        path_to_flash = 'pagapp.public_pages.views.flash'
        path_to_is_upgrade_ready = 'pagapp.public_pages.views.is_upgrade_ready'
        with patch(path_to_first_run) as mock_first_run, \
                patch(path_to_upgrade_database) as mock_upgrade_database, \
                patch(path_to_render_template) as mock_render_template, \
                patch(path_to_flash) as mock_flash, \
                patch(path_to_is_upgrade_ready) as mock_is_upgrade_ready:
            mock_first_run.return_value = False
            mock_is_upgrade_ready.return_value = True
            index()
            self.assertTrue(mock_upgrade_database.called)
            self.assertTrue(mock_flash.called)
            self.assertTrue(mock_render_template.called)
        del mock_configuration
        del mock_albums


class AlbumTestCase(unittest.TestCase):
    """Tests for album() function."""

    @patch('pagapp.public_pages.views.render_template')
    def test_album(self, mock_render_template):
        """Test for album() function.

        Test case:
        If album with given album_url is exists - function should
        return render_template() result.
        """
        test_album_url = 'album_url'
        test_filter_by = 'test_filter_by'
        mock_filter_by_result = MagicMock()
        mock_filter_by_result.first.result_value = test_filter_by

        path_to_pictures = 'pagapp.public_pages.views.Pictures'
        path_to_albums = 'pagapp.public_pages.views.Albums'
        path_to_configuration = 'pagapp.public_pages.views.Configuration'
        with patch(path_to_pictures) as mock_pictures, \
                patch(path_to_albums) as mock_albums, \
                patch(path_to_configuration) as mock_configuration:
            mock_first_result = MagicMock()
            mock_first_result.gallery_title = 'test'
            mock_configuration.query.first.return_value = mock_first_result
            mock_albums.query.filter_by.return_value = mock_filter_by_result
            mock_pictures.query.filter_by.return_value = test_filter_by

            test_render_template_result = 'render_template_result'
            mock_render_template.return_value = test_render_template_result
            self.assertEqual(album(test_album_url), test_render_template_result,
                             msg="render_template() should be called!")

    @patch('pagapp.public_pages.views.current_app')
    @patch('pagapp.public_pages.views.abort')
    @patch('pagapp.public_pages.views.render_template')
    def test_album_no_template(self, mock_render_template, mock_abort,
                               mock_app):
        """Test for album() function.

        Test case:
        If album is exists but HTML template does not exists - function
        should call abort(404).
        """
        test_album_url = 'album_url'
        test_filter_by = 'test_filter_by'
        mock_filter_by_result = MagicMock()
        mock_filter_by_result.first.result_value = test_filter_by

        path_to_albums = 'pagapp.public_pages.views.Albums'
        path_to_pictures = 'pagapp.public_pages.views.Pictures'
        path_to_configuration = 'pagapp.public_pages.views.Configuration'
        with patch(path_to_albums) as mock_albums, \
                patch(path_to_pictures) as mock_pictures, \
                patch(path_to_configuration) as mock_configuration:
            mock_albums.query.filter_by.return_value = mock_filter_by_result
            mock_pictures.query.filter_by.return_value = test_filter_by
            mock_first_result = MagicMock()
            mock_first_result.gallery_title = 'test'
            mock_configuration.query.first.return_value = mock_first_result

            mock_render_template.side_effect = TemplateNotFound(name='test')
            album(test_album_url)
            self.assertTrue(mock_abort.called, msg="abort() not called!")
        del mock_app

    @patch('pagapp.public_pages.views.current_app')
    @patch('pagapp.public_pages.views.url_for')
    @patch('pagapp.public_pages.views.redirect')
    @patch('pagapp.public_pages.views.flash')
    def test_album_not_exists(self, mock_flash, mock_redirect, mock_url_for,
                              mock_app):
        """Test for album() function.

        Test case:
        If album with given album_url does not exists - function should
        catch AttributeError exception and call flash() and redirect()
        function.
        """
        test_album_url = 'album_url'
        test_filter_by = 'test_filter_by'
        mock_filter_by_result = MagicMock()
        mock_filter_by_result.first.result_value = test_filter_by

        path_to_albums = 'pagapp.public_pages.views.Albums'
        path_to_pictures = 'pagapp.public_pages.views.Pictures'
        with patch(path_to_albums) as mock_albums, \
                patch(path_to_pictures) as mock_pictures:
            mock_albums.query.filter_by.return_value = mock_filter_by_result
            mock_pictures.query.filter_by.return_value = test_filter_by
            mock_albums.query.filter_by.side_effect = AttributeError()

            redirect_result = 'test redirect'
            url_for_result = 'test url for'
            mock_redirect.return_value = redirect_result
            mock_url_for.return_value = url_for_result

            self.assertEqual(album(test_album_url), redirect_result,
                             msg="redirect() should be called!")
            self.assertTrue(mock_flash.called, msg="flash() does not called!")
        del mock_app


class LoginTestCase(unittest.TestCase):
    """Tests for login() function."""

    @patch('pagapp.public_pages.views.current_app')
    @patch('pagapp.public_pages.views.redirect')
    @patch('pagapp.public_pages.views.url_for')
    @patch('pagapp.public_pages.views.login_user')
    @patch('pagapp.public_pages.views.request')
    def test_login(self, mock_request, mock_login_user, mock_url_for,
                   mock_redirect, mock_app):
        """Test for login() function.

        Test case:
        If request.method equals with 'POST' and login form validated
        successfully - login_user() should be called and function
        should return result of redirect() call.
        """
        mock_filter_by_result = MagicMock()
        mock_filter_by_result.first.return_value = 'test'
        path_to_users = 'pagapp.public_pages.views.Users'
        path_to_current_user = 'pagapp.public_pages.views.current_user'
        path_to_login_form = 'pagapp.public_pages.views.LoginForm'

        with patch(path_to_users) as mock_users, \
                patch(path_to_current_user) as mock_user, \
                patch(path_to_login_form) as mock_login_form:
            mock_request.method = 'POST'
            mock_request.args.get.return_value = None
            mock_login_form.return_value.validate.return_value = True
            mock_login_form.return_value.login.data = 'test'

            mock_user.is_authenticated.return_value = False

            mock_users.query.filter_by.return_value = mock_filter_by_result

            redirect_result = 'test redirect'
            mock_redirect.return_value = redirect_result

            self.assertEqual(login(), redirect_result,
                             msg="redirect() should be called")
            self.assertTrue(mock_login_user.called,
                            msg="login_user() should be called!")
            self.assertTrue(mock_url_for.called,
                            msg="url_for() should be called!")
        del mock_app

    @patch('pagapp.public_pages.views.current_app')
    @patch('pagapp.public_pages.views.render_template')
    @patch('pagapp.public_pages.views.flash_form_errors')
    @patch('pagapp.public_pages.views.request')
    def test_login_not_post(self, mock_request, mock_flash_form_errors,
                            mock_render_template, mock_app):
        """Test for login() function.

        Test case:
        If request.method not equals with 'POST' - flash_form_errors() should
        be called. Also function should return render_template() call result.
        """
        path_to_users = 'pagapp.public_pages.views.Users'
        path_to_configuration = 'pagapp.public_pages.views.Configuration'
        path_to_login_form = 'pagapp.public_pages.views.LoginForm'
        path_to_current_user = 'pagapp.public_pages.views.current_user'
        with patch(path_to_users) as mock_users, \
                patch(path_to_configuration) as mock_configuration, \
                patch(path_to_login_form) as mock_login_form, \
                patch(path_to_current_user) as mock_user:
            mock_filter_by_result = MagicMock()
            mock_first_result = MagicMock()
            mock_filter_by_result.first.return_value = 'test'
            mock_first_result.gallery_title = 'test'
            mock_users.query.filter_by.return_value = mock_filter_by_result
            mock_configuration.query.first.return_value = mock_first_result

            mock_user.is_authenticated.return_value = False

            mock_request.method = 'GET'
            mock_login_form.return_value.validate.return_value = True
            mock_login_form.return_value.login.data = 'test'

            render_template_result = 'render_template result'
            mock_render_template.return_value = render_template_result
            self.assertEqual(login(), render_template_result,
                             msg="render_template() should be called")
            self.assertTrue(mock_flash_form_errors.called)
        del mock_app

    @patch('pagapp.public_pages.views.current_app')
    @patch('pagapp.public_pages.views.render_template')
    @patch('pagapp.public_pages.views.flash_form_errors')
    @patch('pagapp.public_pages.views.request')
    def test_login_not_validate(self, mock_request, mock_flash_form_errors,
                                mock_render_template, mock_app):
        """Test for login() function.

        Test case:
        If login form does not validate - flash_form_errors() should
        be called. Also function should return render_template() call result.
        """
        path_to_users = 'pagapp.public_pages.views.Users'
        path_to_login_form = 'pagapp.public_pages.views.LoginForm'
        path_to_configuration = 'pagapp.public_pages.views.Configuration'
        path_to_current_user = 'pagapp.public_pages.views.current_user'
        with patch(path_to_users) as mock_users, \
                patch(path_to_login_form) as mock_login_form, \
                patch(path_to_configuration) as mock_configuration, \
                patch(path_to_current_user) as mock_user:
            mock_first_result = MagicMock()
            mock_filter_by_result = MagicMock()
            mock_filter_by_result.first.return_value = 'test'
            mock_first_result.gallery_title = 'test'
            mock_users.query.filter_by.return_value = mock_filter_by_result
            mock_configuration.query.first.return_value = mock_first_result

            mock_user.is_authenticated.return_value = False

            mock_request.method = 'POST'
            mock_login_form.return_value.validate.return_value = False
            mock_login_form.return_value.login.data = 'test'

            render_template_result = 'render_template result'
            mock_render_template.return_value = render_template_result
            self.assertEqual(login(), render_template_result,
                             msg="render_template() should be called")
            self.assertTrue(mock_flash_form_errors.called)
        del mock_app

    @patch('pagapp.public_pages.views.current_app')
    @patch('pagapp.public_pages.views.render_template')
    @patch('pagapp.public_pages.views.flash_form_errors')
    @patch('pagapp.public_pages.views.request')
    def test_login_not_post_validate(self, mock_request, mock_flash_form_errors,
                                     mock_render_template, mock_app):
        """Test for login() function.

        Test case:
        If request.method not equals with 'POST' and login form does not
        validate - flash_form_errors() should be called. Also function
        should return render_template() call result.
        """
        path_to_users = 'pagapp.public_pages.views.Users'
        path_to_configuration = 'pagapp.public_pages.views.Configuration'
        path_to_login_form = 'pagapp.public_pages.views.LoginForm'
        path_to_current_user = 'pagapp.public_pages.views.current_user'
        with patch(path_to_users) as mock_users, \
                patch(path_to_configuration) as mock_configuration, \
                patch(path_to_login_form) as mock_login_form, \
                patch(path_to_current_user) as mock_user:
            mock_filter_by_result = MagicMock()
            mock_first_result = MagicMock()
            mock_filter_by_result.first.return_value = 'test'
            mock_first_result.gallery_title = 'test'
            mock_users.query.filter_by.return_value = mock_filter_by_result
            mock_configuration.query.first.return_value = mock_first_result

            mock_user.is_authenticated.return_value = False

            mock_request.method = 'GET'
            mock_login_form.return_value.validate.return_value = False
            mock_login_form.return_value.login.data = 'test'

            render_template_result = 'render_template result'
            mock_render_template.return_value = render_template_result
            self.assertEqual(login(), render_template_result,
                             msg="render_template() should be called")
            self.assertTrue(mock_flash_form_errors.called)
        del mock_app

    @patch('pagapp.public_pages.views.current_app')
    @patch('pagapp.public_pages.views.abort')
    @patch('pagapp.public_pages.views.render_template')
    @patch('pagapp.public_pages.views.flash_form_errors')
    @patch('pagapp.public_pages.views.request')
    def test_login_no_template(self, mock_request, mock_flash_form_errors,
                               mock_render_template, mock_abort, mock_app):
        """Test for login() function.

        Test case:
        If request.method not equals with 'POST' - flash_form_errors() should
        be called. Also if HTML template not exists abort(404) should be
        called.
        """
        path_to_users = 'pagapp.public_pages.views.Users'
        path_to_configuration = 'pagapp.public_pages.views.Configuration'
        path_to_login_form = 'pagapp.public_pages.views.LoginForm'
        path_to_current_user = 'pagapp.public_pages.views.current_user'
        with patch(path_to_users) as mock_users, \
                patch(path_to_login_form) as mock_login_form, \
                patch(path_to_configuration) as mock_configuration, \
                patch(path_to_current_user) as mock_user:
            mock_filter_by_result = MagicMock()
            mock_first_result = MagicMock()
            mock_filter_by_result.first.return_value = 'test'
            mock_first_result.gallery_title = 'test'
            mock_users.query.filter_by.return_value = mock_filter_by_result
            mock_configuration.query.first.return_value = mock_first_result

            mock_user.is_authenticated.return_value = False

            mock_request.method = 'GET'
            mock_login_form.return_value.validate.return_value = False
            mock_login_form.return_value.login.data = 'test'

            mock_render_template.side_effect = TemplateNotFound(name='test')
            login()
            self.assertTrue(mock_abort.called, msg="abort() should be called!")
            self.assertTrue(mock_flash_form_errors.called)
        del mock_app

    @patch('pagapp.public_pages.views.redirect')
    @patch('pagapp.public_pages.views.url_for')
    @patch('pagapp.public_pages.views.current_user')
    def test_login_user_already_authenticated(self, mock_user, mock_url_for,
                                              mock_redirect):
        """Test for login() function.

        Test case:
        If user already logged in - user should be redirected to
        the admin's panel.
        """
        mock_user.is_authenticated.return_value = True
        login()
        self.assertTrue(mock_url_for.called)
        self.assertTrue(mock_redirect.called)
        mock_url_for.assert_called_with('admin_panel.panel')

    @patch('pagapp.public_pages.views.login_user')
    @patch('pagapp.public_pages.views.current_app')
    @patch('pagapp.public_pages.views.request')
    def test_login_open_request(self, mock_request, mock_app, mock_login_user):
        """Test for login() function.

        Test case:
        If someone passed some extra arguments to the request - function
        should call abort() immediately.
        """
        mock_filter_by_result = MagicMock()
        mock_filter_by_result.first.return_value = 'test'
        path_to_users = 'pagapp.public_pages.views.Users'
        path_to_current_user = 'pagapp.public_pages.views.current_user'
        path_to_login_form = 'pagapp.public_pages.views.LoginForm'
        path_to_abort = 'pagapp.public_pages.views.abort'

        with patch(path_to_current_user) as mock_user, \
                patch(path_to_login_form) as mock_login_form, \
                patch(path_to_users) as mock_users, \
                patch(path_to_abort) as mock_abort:
            mock_request.method = 'POST'
            mock_login_form.return_value.validate.return_value = True
            mock_login_form.return_value.login.data = 'test'
            mock_user.is_authenticated.return_value = False

            mock_users.query.filter_by.return_value = mock_filter_by_result

            mock_request.args.get.return_value = 'test'

            login()
            self.assertTrue(mock_abort.called)
            mock_abort.assert_called_with(400)
        del mock_app
        del mock_login_user


if __name__ == '__main__':
    unittest.main()
