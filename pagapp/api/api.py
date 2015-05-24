"""Handlers for API calls."""

import json
from flask_login import login_required

from pagapp.api import api
from pagapp.models.albums import Albums
from pagapp.models.pictures import Pictures


@api.route('/get-albums-list')
def get_albums_list():
    """Returns list of albums.

    Returns JSON array, which contains list
    of albums. Sample result:
    [
        {
            'name': u'Test album name',
            'pics_count': 1,
            'delete': u'button'
        }
    ]
    """
    return json.dumps(
        [
            {
                'name': album.album_name,
                'pics_count': Pictures.query.filter_by(
                    album_id=album.id).count(),
                'description': album.album_description,
                'delete': u'<b>test</b>'
            } for album in Albums.query.all()
        ]
    )
