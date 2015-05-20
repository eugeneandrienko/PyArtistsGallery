"""Package with descriptions of database tables.

Modules inside:
albums -- has inside description of "albums" table.
users -- has inside description of "users" table.
pictures -- has inside description of "pictures" table.
configuration -- has inside description of "configuration" table.
"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

__all__ = ['albums', 'pictures', 'users',
           'configuration']
