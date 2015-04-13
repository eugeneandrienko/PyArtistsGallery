"""Package with different views for Flask application.

Modules inside:
albums -- contains views, related to album's operations.
main -- contains main view (/index and /).
upload -- contains view, related to uploading new pictures.
users -- contains views, which using for user-related operations.
"""

from pagapp.views import albums
from pagapp.views import main
from pagapp.views import upload
from pagapp.views import users


__all__ = ['albums', 'main', 'upload', 'users']


def warning_killer():
    pass
