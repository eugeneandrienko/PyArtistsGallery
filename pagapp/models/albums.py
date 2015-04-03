from pagapp import db


class Albums(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url_part = db.Column(db.String(), index=True, unique=True, nullable=False)
    album_name = db.Column(db.String(), index=True, unique=False,
        nullable=False)
    album_description = db.Column(db.String(), index=True, unique=False,
        nullable=True)

    def get_url_part(self):
        return self.url_part

    def get_album_name(self):
        return self.album_name

    def get_album_description(self):
        return self.album_description

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
                    'url_part': album.get_url_part(),
                    'album_name': album.get_album_name(),
                    'album_description': album.get_album_description()
                }
            )
        return result

    def set_new_album_name(self, new_name):
        self.album_name = new_name

    def set_new_album_descr(self, new_desc):
        self.album_description = new_desc
