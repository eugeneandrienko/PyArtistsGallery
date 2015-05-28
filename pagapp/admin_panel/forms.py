"""Set of forms which using in admin panel.

List of forms:
ChangePasswordForm -- providing form for password change.
AddAlbumForm -- providing form for adding new album.
UploadForm -- providing form for uploading new pictures.
"""

from flask import current_app
from flask_login import current_user
from flask_wtf import Form
from flask_wtf.form import ValidationError
from wtforms import PasswordField, SubmitField, StringField, FileField, \
    SelectField
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
        del form
        if current_user.check_password(field.data) is False:
            current_app.logger.error(
                "User provided wrong password, when (s)he tried to change it.")
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


class UploadForm(Form):
    """Form for uploading new pictures to the given album."""

    file_names = FileField(
        "Select files:",
        # validators=None,
        id='inputFiles',
        description="Select files")
    album = SelectField(
        "Select album:",
        choices=[],
        id='selectAlbum',
        description="Select album")
    submit_button = SubmitField("Upload")
