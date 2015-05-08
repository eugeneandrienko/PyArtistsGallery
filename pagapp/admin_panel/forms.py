"""Set of forms which using in admin panel.

List of forms:
ChangePasswordForm -- providing form for password change.
"""

from flask_login import current_user
from flask_wtf import Form
from flask_wtf.form import ValidationError
from wtforms import PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo


class ChangePasswordForm(Form):
    """Form for changing password for current user."""

    old_password = PasswordField(
        "Current password:",
        validators=[DataRequired()],
        description="Current password")
    new_password = PasswordField(
        "New password:",
        validators=[DataRequired()],
        description="New password")
    new_password2 = PasswordField(
        "Retype new password:",
        validators=[DataRequired(),
                    EqualTo('new_password',
                            message="Passwords must match")],
        description="New password")
    submit_button = SubmitField('Change password')

    @staticmethod
    def validate_old_password(form, field):
        """Check, is given current password is not wrong."""
        if current_user.check_password(field.data) is False:
            raise ValidationError("Given password is wrong")