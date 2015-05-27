"""Handlers for API calls."""

import json
from flask import request, current_app
from flask_login import login_required

from pagapp.support_functions import remove_danger_symbols
from pagapp.application_api import application_api
from pagapp.models import db
from pagapp.models.albums import Albums
from pagapp.models.pictures import Pictures


def _generate_action_buttons(album):
    edit_button = '<button {}>Edit</button>'.format(
        'type="button" ' +
        'class="btn-xs btn-default" ' +
        'data-toggle="modal" ' +
        'data-target="#editAlbumModal" ' +
        'data-id="' + str(album.id) + '" ' +
        'data-name="' + str(album.album_name) + '" ' +
        'data-description="' + str(album.album_description) + '" ')
    delete_button = '<button {}>Delete</button>'.format(
        'class="btn-xs btn-danger" ' +
        'onclick="deleteAlbum(' + str(album.id) + ')"')
    return '<div class="container-fluid">' + \
           '<div class="btn-toolbar" role="toolbar">' + \
           '<div class="btn-group" role="group">' + \
           edit_button + \
           '</div>' + \
           '<div class="btn-group" role="group">' + \
           delete_button + \
           '</div>' + \
           '</div>' + \
           '</div>'


def _generate_album_table_item(album):
    return {
        'name': album.album_name,
        'pics_count': Pictures.query.filter_by(album_id=album.id).count(),
        'description': album.album_description,
        'actions': _generate_action_buttons(album)
    }


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
        [_generate_album_table_item(album) for album in Albums.query.all()])


@application_api.route('/delete-album', methods=['POST'])
@login_required
def delete_album():
    """Deletes album with given ID if it is one album in database."""
    album_id = remove_danger_symbols(request.form['album_id'])
    album = Albums.query.filter_by(id=album_id)
    if album.count() != 1:
        current_app.logger.error(
            "Count of albums with given ID ({}) is more than 1.".format(
                album_id))
        return '', 404
    else:
        current_app.logger.debug("Deleting album with ID {}.".format(album_id))
        db.session.delete(album.first())
        db.session.commit()
    return '', 200


@application_api.route('/edit-album', methods=['POST'])
@login_required
def edit_album():
    """Edit album with given ID, name and description."""
    album_id = remove_danger_symbols(request.form['album_id'])
    album = Albums.query.filter_by(id=album_id)

    if album.count() == 0:
        current_app.logger.error(
            "Album with given ID ({}) does not exists.".format(album_id))
        return 'Album does not exists!', 404
    if album.count() != 1:
        current_app.logger.error(
            "Count of albums with given ID ({}) is more than 1.".format(
                album_id))
        return 'Cannot delete album, error with ID!', 404

    album_name = remove_danger_symbols(request.form['album_name'])
    album_description = remove_danger_symbols(request.form['album_description'])

    current_app.logger.debug(
        "Editing album with ID {}. New name: {}. New description: {}.".format(
            album_id, album_name, album_description))
    album.first().album_name = album_name
    album.first().album_description = album_description
    db.session.commit()
    return '', 200
