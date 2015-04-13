"""Package with descriptions of database tables.

Modules inside:
albums -- has inside description of "albums" table.
users -- has inside description of "users" table.
pictures -- has inside descriptiom of "pictures" table.
"""

from pagapp.models.albums import Albums
from pagapp.models.users import Users
from pagapp.models.pictures import Pictures


__all__ = ['albums', 'pictures', 'users']