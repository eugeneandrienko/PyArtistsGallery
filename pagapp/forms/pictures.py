"""Set of forms for manipulating with pictures in gallery.

 List of forms:
 PictureForm -- service form, which returns list of pictires
 inside album with given album ID.
 """

from pagapp.models.pictures import Pictures


class PictureForm:
    """Service form for obtaining list of pictures within given album."""

    @staticmethod
    def get_pictures(album_id):
        """Returns list of pictures within album with given album ID.

        Argument:
        album_id -- identifies album from which pictures will be returned.

        Return value:
        Returns instances of pagapp.models.Pictures with given album ID.
        """
        return Pictures.query.filter_by(album_id=album_id)
