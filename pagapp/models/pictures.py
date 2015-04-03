from pagapp import db


class Pictures(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    album_id = db.Column(db.Integer, db.ForeignKey('albums.id'))
    path_to_image = db.Column(db.String(), index=True, nullable=False)
    path_to_thumb = db.Column(db.String(), index=True, nullable=False)
    name = db.Column(db.String(), index=True, nullable=False)
    upload_date = db.Column(db.DateTime(), index=True, nullable=False)
    uploader_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, album_id, uploader_id, upload_date, path_to_image,
                 path_to_thumb, name=''):
        self.album_id = album_id
        self.path_to_image = path_to_image
        self.path_to_thumb = path_to_thumb
        self.name = name
        self.upload_date = upload_date
        self.uploader_id = uploader_id

    def __repr__(self):
        return 'Album ID: {}, Uploader ID: {}, Date: {}, Path: {}|{}, ' \
               'Name: {}'.format(str(self.album_id),
                                 str(self.uploader_id),
                                 str(self.upload_date),
                                 self.path_to_image,
                                 self.path_to_thumb,
                                 self.name)
