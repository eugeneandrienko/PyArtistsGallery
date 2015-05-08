"""Form, using in blueprint with public pages.

This module contains simple login form.
"""

from flask_wtf import Form
from flask_wtf.form import ValidationError
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

from pagapp.models.users import Users


class LoginForm(Form):
    """Form, where user can enter login and password.

    Form provides two fields: for login and for password and validates
    entered credentials.
    """

    login = StringField(
        "Login name:",
        validators=[DataRequired()],
        description="Login name")
    password = PasswordField(
        "Password:",
        validators=[DataRequired()],
        description="Password")
    submit_button = SubmitField(
        "Let me in",
        description="Login button")

    @staticmethod
    def validate_login(form, field):
        """Login field validator."""
        user = Users.query.filter_by(
            nickname=field.data).first()
        if user is None:
            raise ValidationError('User %s does not exists in the database' %
                                  field.data)

    @staticmethod
    def validate_password(form, field):
        """Password field validator.

        If given password does not match with user's password from
        database - send warning to user.
        """
        user = Users.query.filter_by(
            nickname=form.login.data).first()
        if user is not None:
            if user.check_password(field.data) is False:
                raise ValidationError('Given password is wrong')
