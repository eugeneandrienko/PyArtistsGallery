from flask.ext.wtf import Form
from flask.ext.login import current_user
from wtforms import PasswordField
from wtforms.validators import DataRequired
from pagapp.models import Users


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
