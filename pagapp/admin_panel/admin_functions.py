"""Functions, which performs administrator's tasks.

Functions, which able to delete, edit, create albums, change password
for current user and so on.
"""

import string
import random
import re

from flask import request, flash
from flask_login import current_user

from pagapp.models import db
from pagapp.models.albums import Albums
from pagapp.support_functions import flash_form_errors, remove_danger_symbols


def change_password(form):
    """Changes password for current user."""
    if form.submit_button.data is False:
        return

    if request.method == 'POST' and form.validate():
        new_password = remove_danger_symbols(form.new_password.data)
        current_user.set_new_password(new_password)
        db.session.commit()
        flash("Password successfully changed", category='success')
    else:
        flash_form_errors(form)


def add_new_album(form):
    """Adds new album to database."""
    if form.submit_button.data is False:
        return

    if request.method == 'POST' and form.validate():
        album_name = remove_danger_symbols(form.album_name.data)
        album_description = remove_danger_symbols(form.album_description.data)

        url_part = album_name.lower()
        url_part = url_part.strip(string.punctuation)
        whitespace_re = re.compile('[' + string.whitespace + ']')
        url_part = whitespace_re.sub('-', url_part)

        if Albums.query.filter_by(url_part=url_part).count() != 0:
            url_part += ''.join(
                random.choice(
                    string.ascii_letters + string.digits
                ) for _ in range(5))

        new_album = Albums(url_part, album_name, album_description)

        db.session.add(new_album)
        db.session.commit()
        flash("New album successfully added.", category='success')
    else:
        flash_form_errors(form)

    # Clear form input fields to show placeholders.
    form.album_name.data = ''
    form.album_description.data = ''
