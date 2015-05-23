"""Set of forms which using in admin panel.

List of forms:
ChangePasswordForm -- providing form for password change.
AddAlbumForm -- providing form for adding new album.
"""

from flask_login import current_user
from flask_wtf import Form
from flask_wtf.form import ValidationError
from wtforms import PasswordField, SubmitField, StringField
from wtforms.validators import DataRequired, EqualTo

from pagapp.models.albums import Albums


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
        del form
        if current_user.check_password(field.data) is False:
            raise ValidationError("Given password is wrong")


class AddAlbumForm(Form):
    """Form for adding new album."""

    album_name = StringField(
        "Name of the new album",
        validators=[DataRequired()],
        description="Name of the new album")
    album_description = StringField(
        "Album's description",
        validators=[DataRequired()],
        description="Short description")
    submit_button = SubmitField("Create")

    @staticmethod
    def validate_album_name(form, field):
        """Check, is given album name does not exists."""
        if Albums.query.filter_by(album_name=field.data).count() != 0:
            raise ValidationError("album {} already exists!".format(field.data))
        del form
