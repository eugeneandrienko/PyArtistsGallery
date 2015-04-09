from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired
from flask_wtf import Form
from flask_login import current_user, login_user

from pagapp import db
from pagapp.models import Users


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
        login_user(self.user)
        return True


class ChangePasswordForm(Form):
    old_password = PasswordField('old_password', validators=[DataRequired()])
    new_password = PasswordField('new_password', validators=[DataRequired()])
    new_password2 = PasswordField('new_password2', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        if current_user is None:
            return False

        if not current_user.check_password(self.old_password.data):
            return False

        if self.new_password.data != self.new_password2.data:
            return False

        current_user.set_new_password(self.new_password.data)
        db.session.commit()
        return True