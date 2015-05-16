"""Functions, which performs administrator's tasks.

Functions, which able to delete, edit, create albums, change password
for current user and so on.
"""

from flask import request, flash
from flask_login import current_user

from pagapp.models import db
from pagapp.support_functions import flash_form_errors


def change_password(form):
    """Changes password for current user."""
    if request.method == 'POST' and form.validate():
        current_user.set_new_password(form.new_password.data)
        db.session.commit()
        flash("Password successfully changed", category='success')
    else:
        flash_form_errors(form)
