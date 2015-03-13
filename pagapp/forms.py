from flask.ext.wtf import Form
from flask.ext.login import current_user
from wtforms import StringField, PasswordField, SelectField, TextAreaField
from wtforms.validators import DataRequired
from pagapp.models import Users
from pagapp.models import Albums


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


class PasswdForm(Form):
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


class NewAlbumForm(Form):
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
    album_select = SelectField('album_select', [])
    album_new_name = StringField('album_new_name')
    album_description = TextAreaField('album_description')

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
