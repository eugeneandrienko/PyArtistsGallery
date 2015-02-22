from flask.ext.wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired
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
        return True

    def get_logged_in_user(self):
        return self.user
