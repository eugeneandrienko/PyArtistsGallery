"""Set of forms for manipulating with albums.

Set of forms for managing albums -- add new album, delete or edit them.

List of forms:
AlbumForm -- service form.
AddAlbumForm -- form for add new album.
EditAlbumNameForm -- form for edit name of existing album.
EditAlbumDescriptionForm -- form for edit description of existing album.
DeleteAlbumForm -- form for delete existing album.
"""

import re
import random
import string

# TODO: use SubmitField everywhere!!!
from wtforms import StringField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf import Form

from pagapp import db
from pagapp.models import Albums


class AlbumForm():
    """Service form -- using for obtaining all existing albums."""

    matched_album = None

    def __init__(self, album_url=None):
        """Performs search of given album's URL.

        Performs search of album if got album URL or does
        nothing if got None.

        Argument:
        album_url -- album's URL as it given in database.
        """
        if album_url is not None:
            self.matched_album = Albums.query.filter_by(
                url_part=album_url).first()

    @staticmethod
    def get_albums_list():
        """Returns all albums from database.

        Return value:
        List of albums from DB.
        Format: ({'url_part': album's URL, 'album_name': name,
        'album_description': description}, {...}, ...).
        """
        return Albums.get_albums_list()


class AddAlbumForm(Form):
    """Form for adding new album."""

    new_album = StringField('new_album', validators=[DataRequired()])
    new_album_description = TextAreaField('new_album_description')
    submit_button = SubmitField('Create new album')

    def validate(self):
        """Extended form validator -- adds new album to database if all ok."""
        rv = Form.validate(self)
        if not rv:
            return False

        album = Albums.query.filter_by(
            album_name=self.new_album.data).first()

        if album is not None:
            return False

        new_album = Albums(
            re.sub(r'[^\w]', '',
                   self.new_album.data.lower()) +
            ''.join(random.choice(string.ascii_lowercase) for i in range(5)),
            self.new_album.data,
            self.new_album_description.data)
        db.session.add(new_album)
        db.session.commit()

        return True


class EditAlbumNameForm(Form):
    """Form for editing name of existing album."""

    album_select = SelectField('album_select', [])
    album_name = StringField('album_name', validators=[DataRequired()])
    submit_button = SubmitField('Save')

    def __init__(self, *args, **kwargs):
        """Extends default constructor with select updater."""
        Form.__init__(self, *args, **kwargs)
        self.update_select_choices()

    def update_select_choices(self):
        """Updater for album's select field."""
        albums_names_array = []
        for album in Albums.get_albums_list():
            albums_names_array.append((album['album_name'],
                                       album['album_name']))
        self.album_select.choices = albums_names_array

    def validate(self):
        """Extended form validator -- changing name of selected album."""
        rv = Form.validate(self)
        if not rv:
            return False

        album = Albums.query.filter_by(
            album_name=self.album_select.data).first()
        if album is None:
            return False

        album.album_name = self.album_name.data
        db.session.commit()
        self.update_select_choices()
        return True


class EditAlbumDescriptionForm(Form):
    """Form for editing album's description."""

    album_select = SelectField('album_select', [])
    album_description = TextAreaField('album_description')
    submit_button = SubmitField('Save')

    def __init__(self, *args, **kwargs):
        """Extends default constructor with select updater."""
        Form.__init__(self, *args, **kwargs)
        self.update_select_choices()

    def update_select_choices(self):
        """Updater for album's select field."""
        albums_names_array = []
        for album in Albums.get_albums_list():
            albums_names_array.append((album['album_name'],
                                       album['album_name']))
        self.album_select.choices = albums_names_array

    def validate(self):
        """Extended form validator -- changing description of album."""
        rv = Form.validate(self)
        if not rv:
            return False

        album = Albums.query.filter_by(
            album_name=self.album_select.data).first()
        if album is None:
            return False

        album.album_description = self.album_description.data
        db.session.commit()
        self.update_select_choices()
        return True


class DeleteAlbumForm(Form):
    """Form for delete existing album."""

    album_select = SelectField('album_select', [])
    submit_button = SubmitField('Delete album')

    def __init__(self, *args, **kwargs):
        """Extends default constructor with select updater."""
        Form.__init__(self, *args, **kwargs)
        self.update_select_choices()

    def update_select_choices(self):
        """Updater for album's select field."""
        albums_names_array = []
        for album in Albums.get_albums_list():
            albums_names_array.append((album['album_name'],
                                       album['album_name']))
        self.album_select.choices = albums_names_array

    def validate(self):
        """Extended form validator -- deleting selected album."""
        rv = Form.validate(self)
        if not rv:
            return False

        album = Albums.query.filter_by(
            album_name=self.album_select.data).first()
        if album is None:
            return False

        db.session.delete(album)
        db.session.commit()
        self.update_select_choices()
        return True