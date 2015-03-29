from wtforms import StringField, PasswordField, SelectField, TextAreaField
from wtforms.validators import DataRequired
from flask_wtf import Form
from flask_login import current_user

from pagapp.models import Users
from pagapp.models import Albums


# Contents of this module:
#
# User-related forms:
# LoginForm: draws login form for /login path.
# Methods: validate() - custom, checks what given user is present
#                                    in db and given password is valid.
#                       get_logged_in_user() - return models.Users object for
#                                              logged in user.
#   ChPasswdForm: draws "change password" form for /passwd path.
#                 Methods: validate() - custom, checks what current user is in
#                                       DB and what given current password is
#                                       in DB and new password is valid.
#                          get_new_password() - returns new password, given by
#                                               user.
# Album-related forms:
#   NewAlbumForm: draws form for new album creation.
#                 Methods: validate() - custom, checks what given album name
#                                       does not present.
#   EditAlbumForm: draws form for edit current album.
#                  Methods: # TODO: incomplete!
#   DeleteAlbumForm: # TODO: incomplete!
# Picture-related forms:
#   # TODO: incomplete!


#
# User-related forms:
#


class LoginForm(Form):
    login = StringField('login', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.user = None

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        user = Users.query.filter_by(
            nickname=self.login.data).first()
        if user is None:
            return False
        if not user.check_password(self.password.data):
            return False

        self.user = user
        return True

    def get_logged_in_user(self):
        return self.user


class ChPasswdForm(Form):
    old_password = PasswordField('old_password', validators=[DataRequired()])
    new_password = PasswordField('new_password', validators=[DataRequired()])
    new_password2 = PasswordField('new_password2', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        # Check - is logged in user is inside db and active
        if current_user is None:
            return False

        if not current_user.check_password(self.old_password.data):
            return False

        if self.new_password.data != self.new_password2.data:
            return False

        return True

    def get_new_password(self):
        return self.new_password.data


#
# Album-related forms:
#


class AddAlbumForm(Form):
    new_album = StringField('login', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        album = Albums.query.filter_by(
            album_name=self.new_album.data)

        if album is None:
            return True

        return False


class EditAlbumForm(Form):
    # TODO: check given album name for existece in DB.
    # TODO: check given new album name for non-existence in DB.
    album_select = SelectField('album_select', [])
    album_new_name = StringField('album_new_name')
    album_description = TextAreaField('album_description')

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)


class DeleteAlbumForm(Form):
    # TODO: check given album name for existence in DB.
    album_select = SelectField('album_select', [])

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)


#
# Picture-related forms:
#

# TODO: incomplete!

#
# Different service forms
#

# Fake form which using for redirect to /upload.
# Usual <a href="..." role="button" ...>...</a>
# do not work inside bootstrap's nav bar.
class GotoUploadFakeForm(Form):
    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)