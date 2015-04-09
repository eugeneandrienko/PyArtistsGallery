from pagapp.models import Pictures


class PictureForm():
    @staticmethod
    def get_pictures(album_id):
        return Pictures.query.filter_by(album_id=album_id)
