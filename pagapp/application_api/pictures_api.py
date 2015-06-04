"""Handlers for pictures' API calls"""

from flask import request
from flask_login import login_required

from pagapp.application_api import application_api


@application_api.route('/get-pictures-list', methods=['POST'])
@login_required
def get_pictures_list():
    """Returns list of pictures.

    Returns JSON array, which contains
    list of pictures from one album.
    Album ID can be found within POST request.
    Sample result:
    """
    print(request.json['album_id'])
    return 'test', 200
