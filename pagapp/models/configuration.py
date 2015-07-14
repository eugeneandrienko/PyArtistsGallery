"""Description of 'Configuration' table from database.

List of classes:
Configuration - contains description of table.
"""

from pagapp.models import db


class Configuration(db.Model):
    """Class with description of 'configuration' table.

    This table contains next fields:
    id -- id of record.
    gallery_title -- title name of installed gallery.
    gallery_description -- obviously, it is gallery description.

    This table can contain only one row - all another rows
    (two, three, etc) will be ignored.
    """

    id = db.Column(db.Integer, primary_key=True)
    gallery_title = db.Column(db.String(128), nullable=False,
                              default='Default title')
    gallery_description = db.Column(db.String(), nullable=False,
                                    default='Default description')

    def __init__(self, gallery_title, gallery_description):
        """Saves user-provided data in the database.

        Arguments:
        gallery_title -- title of installed gallery.
        gallery_description -- description of installed gallery.
        """
        self.gallery_title = gallery_title
        self.gallery_description = gallery_description

    def __repr__(self):
        """Prints instance contents in debug session."""
        return 'Title: {}, Description: {}'.format(
            self.gallery_title, self.gallery_description)
