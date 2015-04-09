from pagapp import db


class Albums(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url_part = db.Column(db.String(), index=True, unique=True, nullable=False)
    album_name = db.Column(
        db.String(), index=True, unique=False, nullable=False)
    album_description = db.Column(
        db.String(), index=True, unique=False, nullable=True)

    def __init__(self, url_part, album_name, album_description):
        self.url_part = url_part
        self.album_name = album_name
        self.album_description = album_description

    def __repr__(self):
        return 'URL part: {}, Album: {}, Description: {}'.format(
            self.url_part,
            self.album_name,
            self.album_description)

    @classmethod
    def get_albums_list(cls):
        result = []
        for album in cls.query.all():
            result.append(
                {
                    'url_part': album.url_part,
                    'album_name': album.album_name,
                    'album_description': album.album_description
                })
        return result