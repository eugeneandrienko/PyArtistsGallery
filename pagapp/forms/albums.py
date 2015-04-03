import re
import random
import string

# TODO: use SubmitField everywhere!!!
from wtforms import StringField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf import Form
from pagapp import db
from pagapp.models.albums import Albums


class AlbumForm():
    matched_album = None

    def __init__(self, albumurl=None):
        if albumurl is not None:
            self.matched_album = Albums.query.filter_by(
                url_part=albumurl).first()

    def get_matched_album(self):
        return self.matched_album

    @staticmethod
    def get_album_list():
        return Albums.get_albums_list()


class AddAlbumForm(Form):
    new_album = StringField('new_album', validators=[DataRequired()])
    new_album_description = TextAreaField('new_album_description')
    submit_button = SubmitField('Create new album')

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
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

    def get_new_album_name(self):
        return self.new_album.data


class EditAlbumNameForm(Form):
    album_select = SelectField('album_select', [])
    album_name = StringField('album_name', validators=[DataRequired()])
    submit_button = SubmitField('Save')

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        albums_names_arr = []
        for album in Albums.get_albums_list():
            albums_names_arr.append((album['album_name'], album['album_name']))
        self.album_select.choices = albums_names_arr

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        album = Albums.query.filter_by(album_name=self.album_select.data
                                       ).first()
        if album is None:
            return False

        album.set_new_album_name(self.album_name.data)
        db.session.commit()
        return True

    def get_old_album_name(self):
        return self.album_select.data

    def get_album_name(self):
        return self.album_name.data


class EditAlbumDescForm(Form):
    album_select = SelectField('album_select', [])
    album_description = TextAreaField('album_description')
    submit_button = SubmitField('Save')

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        albums_names_arr = []
        for album in Albums.get_albums_list():
            albums_names_arr.append((album['album_name'], album['album_name']))
        self.album_select.choices = albums_names_arr

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        album = Albums.query.filter_by(album_name=self.album_select.data
                                       ).first()
        if album is None:
            return False

        album.set_new_album_descr(self.album_description.data)
        db.session.commit()
        return True

    def get_album_name(self):
        return self.album_select.data


class DeleteAlbumForm(Form):
    album_select = SelectField('album_select', [])
    submit_button = SubmitField('Delete album')

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        albums_names_arr = []
        for album in Albums.get_albums_list():
            albums_names_arr.append((album['album_name'], album['album_name']))
        self.album_select.choices = albums_names_arr

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        album = Albums.query.filter_by(
            album_name=self.album_select.data).first()
        if album is None:
            return False

        db.session.delete(album)
        db.session.commit()
        return True

    def get_album_name(self):
        return self.album_select.data