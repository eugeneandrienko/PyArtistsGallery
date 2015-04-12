"""Description of "pictures" table from database.

List of classes:
Pictures -- contains description of "pictures" table.
"""

import datetime

from pagapp import db


class Pictures(db.Model):
    """Class with description of "pictures" table inside.

    Table "pictures" contains next fields:
    id -- unique id of picture.
    album_id -- id of album, which contain picture inside.
    path_to_image -- path to corresponding image.
    path_to_thumbnail -- path to corresponding thumbnail.
    name -- name of picture.
    upload_date -- date, when picture was uploaded.
    uploader_id -- ud of user, who uploaded picture.
    """

    id = db.Column(db.Integer, primary_key=True)
    album_id = db.Column(db.Integer, db.ForeignKey('albums.id'))
    path_to_image = db.Column(db.String(), index=True, nullable=False)
    path_to_thumbnail = db.Column(db.String(), index=True, nullable=False)
    name = db.Column(db.String(), index=True, nullable=False)
    upload_date = db.Column(db.DateTime(), index=True, nullable=False)
    uploader_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, album_id, uploader_id, upload_date, path_to_image,
                 path_to_thumbnail, name=''):
        """Saves picture data in internal structures.

        Overrides default form constructor.

        Arguments:
        album_id -- id of album, which contains picture.
        uploader_id -- id of user, who uploaded picture.
        upload_date -- date, when picture was uploaded.
        path_to_image -- path to file with picture.
        path_to_thumbnail -- path to file with thumbnail for picture.
        name -- name of the picture.
        """
        self.album_id = album_id
        self.path_to_image = path_to_image
        self.path_to_thumbnail = path_to_thumbnail
        self.name = name
        self.upload_date = upload_date
        self.uploader_id = uploader_id

    def __repr__(self):
        """Prints instance contents in debug session."""
        return 'Album ID: {}, Uploader ID: {}, Date: {}, Path: {}|{}, ' \
               'Name: {}'.format(str(self.album_id),
                                 str(self.uploader_id),
                                 str(self.upload_date),
                                 self.path_to_image,
                                 self.path_to_thumbnail,
                                 self.name)