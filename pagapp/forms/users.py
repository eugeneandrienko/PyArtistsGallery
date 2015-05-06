"""Set of forms for providing user-related features.

List of forms:
LoginForm -- providing login form for administrator.
ChangePasswordForm -- providing form for password change.
"""

from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf import Form
from flask_login import current_user, login_user

from pagapp import db
from pagapp.models.users import Users


class LoginForm(Form):
    """Form, where user can enter login and password.

    Form provides two fields: for login and for password and validates
    given user's credentials.
    """

    login = StringField('login', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    submit_button = SubmitField('Let me in!')

    def __init__(self, *args, **kwargs):
        """Extends default constructor with addition for flask_login"""
        Form.__init__(self, *args, **kwargs)
        self.user = None

    def validate(self):
        """Overrides default validator -- checks given login and password.

        This validator checks given login for existence in database and made
        same check for given password.
        If all is OK, this validator lets the user come in.
        """
        rv = Form.validate(self)
        if not rv:
            return False

        user = Users.query.filter_by(
            nickname=self.login.data).first()
        if user is None:
            return False
        if user.check_password(self.password.data) is False:
            return False

        self.user = user
        login_user(self.user)
        return True


class ChangePasswordForm(Form):
    """Form for changing password for current user."""

    old_password = PasswordField('old_password', validators=[DataRequired()])
    new_password = PasswordField('new_password', validators=[DataRequired()])
    new_password2 = PasswordField('new_password2', validators=[DataRequired()])
    submit_button = SubmitField('Change password')

    def validate(self):
        """Overrides default validator -- this can change user password.

        This validator checks given user password and change it to new if
        all is OK and user is logged in.
        """
        rv = Form.validate(self)
        if not rv:
            return False

        if current_user.is_anonymous():
            return False

        if current_user.check_password(self.old_password.data) is False:
            return False

        if self.new_password.data != self.new_password2.data:
            return False

        current_user.set_new_password(self.new_password.data)
        db.session.commit()
        return True