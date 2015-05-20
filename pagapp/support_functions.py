"""Different support functions for PyArtistsGallery.

I place here some functions, which do not match to any
blueprint or widely use with all blueprints.
"""

from sqlalchemy.orm.exc import ObjectDeletedError
from sqlalchemy.exc import OperationalError
from flask import flash
from flask_login import LoginManager

from pagapp.models.albums import Albums
from pagapp.models.pictures import Pictures
from pagapp.models.users import Users
from pagapp.models.configuration import Configuration

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


def is_first_run():
    """Is application running first time or not.

    Function returns True if schema is broken.
    Also. function returns True if some config fields do
    not filled - in this case we consider, what application
    run at first time.
    Function returns False if all configuration fields in database
    are filled.
    """

    try:
        Albums.query.first()
        Configuration.query.first()
        Pictures.query.first()
        Users.query.first()
    except OperationalError:
        return True

    if len(Configuration.query.all()) == 0:
        return True

    if len(Users.query.all()) == 0:
        return True

    return False
