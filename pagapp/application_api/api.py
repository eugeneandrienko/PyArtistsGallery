"""Handlers for API calls."""

import json
from flask import request
from flask_login import login_required

from pagapp.application_api import application_api
from pagapp.models import db
from pagapp.models.albums import Albums
from pagapp.models.pictures import Pictures


@application_api.route('/get-albums-list')
def get_albums_list():
    """Returns list of albums.

    Returns JSON array, which contains list
    of albums. Sample result:
    [
        {
            'name': u'Test album name',
            'pics_count': 1,
            'description': u'Test album description',
            'delete': u'button HTML code'
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
                'delete': u'<button class="btn-xs btn-danger" ' +
                          'onclick="deleteAlbum(' +
                          str(album.id) +
                          ')">Delete album</button>'
            } for album in Albums.query.all()
        ]
    )

@application_api.route('/delete-album', methods=['POST'])
@login_required
def delete_album():
    album = Albums.query.filter_by(id=request.form['album_id'])
    if album.count() != 1:
        return '', 404
    else:
        db.session.delete(album.first())
        db.session.commit()
    return '', 200
