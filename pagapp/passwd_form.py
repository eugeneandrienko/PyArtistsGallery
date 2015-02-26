from flask.ext.wtf import Form
from wtforms import PasswordField
from wtforms.validators import DataRequired


class PasswdForm(Form):
    old_password = PasswordField('old_password', validators=[DataRequired()])
    new_password = PasswordField('new_password', validators=[DataRequired()])
    new_password2 = PasswordField('new_password2', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
