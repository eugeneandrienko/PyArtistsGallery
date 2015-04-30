"""Tests for forms from pagapp.forms.albums."""

import unittest

from unittest import mock
from flask import Flask

from pagapp.forms import AlbumForm, AddAlbumForm, \
    EditAlbumNameForm, EditAlbumDescriptionForm, DeleteAlbumForm
from pagapp.models import Albums


class _MockFilterByReturnValue():
    """Special mock object for filter_by() function.

    filter_by() function returns object with first() method.
    We use this method inside code of our application.
    """

    first_return_value = None

    def __init__(self, first_return_value=None):
        self.first_return_value = first_return_value

    def first(self):
        """Special method, which uses inside code of out application."""
        return self.first_return_value


class _FormTestCase(unittest.TestCase):
    """Parent for all tests of flask_wtf.Form and it's children."""

    def setUp(self):
        self.app = self.create_app()
        self.client = self.app.test_client()
        self.ctx = self.app.test_request_context()
        self.ctx.push()

    def tearDown(self):
        self.ctx.pop()

    def create_app(self):
        app = Flask(__name__)
        app.secret_key = 'secret'
        return app


class AlbumFormTestCase(unittest.TestCase):
    """Test for AlbumForm form.

    Test cases:
    test_init -- tests __init__() method.
    test_get_albums_list -- tests method, which should return all albums
    from database.
    """

    @mock.patch('pagapp.models.Albums.query')
    def test_init(self, mock_query):
        """Tests __init__() method.

        Test cases:
        If we do not pass any arguments to constructor - matched_album
        field should be equal with None.
        If we pass URL to constructor -- we should call corresponding
        branch of code inside the constructor and initialize matched_album
        field.
        """
        test_album = AlbumForm()
        self.assertEqual(test_album.matched_album, None,
                         msg="matched_album should be None!")
        self.assertFalse(mock_query.filter_by.called,
                         msg="filter_by() should not be called!")

        mock_query.filter_by.return_value = _MockFilterByReturnValue(
            first_return_value='test')
        test_parameter = 'Test321'
        test_album = AlbumForm(test_parameter)
        self.assertNotEqual(test_album.matched_album, None,
                            msg="matched_album should not be None!")
        self.assertTrue(mock_query.filter_by.called,
                        msg="filter_by should be called!")
        mock_query.filter_by.assert_called_with(url_part=test_parameter)

    @mock.patch('pagapp.models.Albums.get_albums_list')
    def test_get_albums_list(self, mock_get_albums_list):
        """Tests get_albums_list() method.

        Test case:
        This method should call get_albums_list() function.
        """
        test_album = AlbumForm()
        test_album.get_albums_list()
        self.assertTrue(mock_get_albums_list.called,
                        msg="get_albums_list() should be called!")


class AddAlbumFormTestCase(_FormTestCase):
    """Test for AddAlbumForm form.

    Test cases:
    test_validate -- test for validate() method.
    """

    @mock.patch('pagapp.models.Albums.query')
    @mock.patch('pagapp.db.session')
    @mock.patch('flask_wtf.Form.validate')
    def test_validate(self, mock_validate, mock_session, mock_query):
        """Tests for _validate() method.

        Test cases:
        If Form.validate() returned False - we should return False too.
        If found Album's object is not None -- validate() should
        return False.
        In other case validate() should return True.
        """
        mock_validate.return_value = False
        test_album_add = AddAlbumForm()
        self.assertFalse(test_album_add.validate(),
                         msg="Form.validate() should return False!")
        mock_validate.return_value = True

        mock_query.filter_by.return_value = _MockFilterByReturnValue(
            first_return_value='test')
        self.assertFalse(test_album_add.validate(),
                         msg="query.filter_by returned something data!")

        mock_query.filter_by.return_value = _MockFilterByReturnValue()
        test_album_add.new_album.data = 'Test'
        test_album_add.new_album_description.data = 'Test'
        self.assertTrue(test_album_add.validate(),
                        msg="query.filter_by returned None!")
        self.assertTrue(mock_session.add.called,
                        msg="db.add() should be called!")
        self.assertTrue(mock_session.commit.called,
                        msg="db.commit() should be called!")


# EditAlbumNameForm, EditAlbumDescriptionForm and DeleteAlbumForm methods
# are the same, that's why I test these classes in one TestCase.
class EditDeleteAlbumFormTestCase(_FormTestCase):
    """Tests for EditAlbumNameForm, EditAlbumDescriptionForm, DeleteAlbumForm.

    Test cases:
    test_validate() -- test for validate() function.
    test_update_select_choices() -- tests albums_select.choices field
    updater.
    """

    @mock.patch('pagapp.models.Albums.query')
    @mock.patch('pagapp.db.session')
    @mock.patch('flask_wtf.Form.validate')
    def test_validate(self, mock_validate, mock_session, mock_query):
        """Test for validate() method.

        Test cases:
        If Form.validate() returns False - we should return False too.
        If found Album object is None - function should return False.
        In other cases we should add data to database and call
        update_select_choices() method.
        """
        for class_ in (EditAlbumNameForm,
                       EditAlbumDescriptionForm,
                       DeleteAlbumForm):
            mock_validate.return_value = False
            test_album = class_()
            self.assertFalse(test_album.validate(),
                             msg="Form.validate() should return False!")
            mock_validate.return_value = True

            mock_query.filter_by.return_value = _MockFilterByReturnValue()
            self.assertFalse(test_album.validate(),
                             msg="_validate() should return False")

            mock_query.filter_by.return_value = _MockFilterByReturnValue(
                first_return_value=Albums('URL', 'name', 'description'))
            self.assertTrue(test_album.validate(),
                            msg="validate() should return True")
            self.assertTrue(mock_session.commit.called,
                            msg="db.session.commit() should be called!")

    @mock.patch('pagapp.models.Albums.get_albums_list')
    def test_update_select_choices(self, mock_get_albums_list):
        """Test for update_select_choices() method.

        Test cases:
        Data from Albums.get_albums_list() should copied to
        albums_select.choices field.
        """
        for class_ in (EditAlbumNameForm,
                       EditAlbumDescriptionForm,
                       DeleteAlbumForm):
            count_of_test_records = 10
            get_albums_list_result = [
                {'album_name': 'TestAlbum' + str(value)} for value in range(
                    0, count_of_test_records)
            ]
            mock_get_albums_list.return_value = get_albums_list_result
            test_album = class_()
            test_album.update_select_choices()
            for i in range(0, count_of_test_records):
                self.assertEqual(
                    get_albums_list_result[i]['album_name'],
                    test_album.album_select.choices[i][0],
                    msg="Returned data is not equal with test data!")
                self.assertEqual(
                    'TestAlbum' + str(i),
                    test_album.album_select.choices[i][1],
                    msg="Returned data is not equal with test data!")


if __name__ == '__main__':
    unittest.main()