"""Description of "albums" table from database.

List of classes:
Albums -- contains description of "albums" table.
"""

from pagapp import db


class Albums(db.Model):
    """Class with description of "albums" table inside.

    Table "albums" contains next fields:
    id -- unique album's ID.
    url_part -- unique string, by which album can be accessed via web
    interface.
    album_name -- name of the album.
    album_description -- description of the album.
    """

    id = db.Column(db.Integer, primary_key=True)
    url_part = db.Column(db.String(), index=True, unique=True, nullable=False)
    album_name = db.Column(
        db.String(), index=True, unique=False, nullable=False)
    album_description = db.Column(
        db.String(), index=True, unique=False, nullable=True)

    def __init__(self, url_part, album_name, album_description):
        """Saves album data in internal structures.

        This constructor overrides default and saves given album's data
        in internal structures. Raises TypeError exception if receives
        argument with wrong type.

        Arguments:
        url_part -- part of URL for accessing the album via web interface.
        album_name -- name of the album.
        album_description -- description of the album.
        """
        if isinstance(url_part, str) and \
                isinstance(album_name, str) and \
                isinstance(album_description, str):
            self.url_part = url_part
            self.album_name = album_name
            self.album_description = album_description
        else:
            raise TypeError('Wrong arguments for Albums constructor!')

    def __repr__(self):
        """Prints instance contents in debug session."""
        return 'URL part: {}, Album: {}, Description: {}'.format(
            self.url_part,
            self.album_name,
            self.album_description)

    @classmethod
    def get_albums_list(cls):
        """Special classmethod, returns list of albums.

        Return value:
        List of albums from database. This list contains dictionaries -- one
        dictionary for one album.
        Format: ({'url_part': album's URL, 'album_name': name,
        'album_description': description}, {...}, ...).
        """
        result = []
        for album in cls.query.all():
            result.append(
                {
                    'url_part': album.url_part,
                    'album_name': album.album_name,
                    'album_description': album.album_description
                })
        return result