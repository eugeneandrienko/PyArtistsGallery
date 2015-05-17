"""Different support functions for PyArtistsGallery.

I place here some functions, which do not match to any
blueprint or widely use with all blueprints.
"""

from sqlalchemy.orm.exc import ObjectDeletedError
from flask import flash
from flask_login import LoginManager

from pagapp.models.users import Users

lm = LoginManager()


@lm.user_loader
def load_user(uid):
    """Loads user by user's ID.

    Argument:
    uid -- user's ID (from database).
    Result:
    User object from database.
    """
    try:
        result = Users.query.get(int(uid))
    except ObjectDeletedError:
        result = None
    return result


def flash_form_errors(form):
    """Shows errors from Flask-WTF form.

    Argument:
    form -- errors will be taken and parsed from this form.
    """
    for field, errors in form.errors.items():
        for error in errors:
            flash(
                "Error in the %s field - %s" % (getattr(form, field).label.text,
                                                error),
                category='warning')
