"""Functions, which help save uploaded files."""

from datetime import datetime
from flask import current_app, flash
from flask_login import current_user
from werkzeug.utils import secure_filename
from os.path import join
from PIL import Image

from pagapp.models import db
from pagapp.models.pictures import Pictures


def _create_thumbnail(path_to_image, path_to_thumbnail):
    """Creates thumbnail from given image.

    Idea of this function was taken from:
    http://united-coders.com/christian-harms/image-resiz
    ing-tips-every-coder-should-know/
    """
    image = Image.open(path_to_image)

    # preresize image with factor 2, 4, 8 and fast algorithm
    factor = 1
    size = current_app.config['THUMBNAIL_SIZE']
    while image.size[0] / factor > 2 * size['x'] and \
            image.size[1] / factor > 2 * size['y']:
        factor *= 2
    if factor > 1:
        image.thumbnail(
            (image.size[0] / factor, image.size[1] / factor), Image.NEAREST)

    image.thumbnail((size['x'], size['y']), Image.ANTIALIAS)
    image.save(path_to_thumbnail)


def save_file(filename_field, album_id, name, description):
    file_name = secure_filename(filename_field.data.filename)

    file_path = join(current_app.config['UPLOAD_FOLDER'], file_name)
    file_path_web = join(
        '../' + current_app.config['UPLOAD_FOLDER_RELATIVE'], file_name)

    thumbnail_path = join(current_app.config['UPLOAD_FOLDER'] + 'thumbnails/',
                          file_name)
    thumbnail_path_web = join(
        '../' + current_app.config['UPLOAD_FOLDER_RELATIVE'] + 'thumbnails/',
        file_name)

    current_app.logger.info("Saving file: " + file_name)

    if Pictures.query.filter_by(path_to_image=file_path_web).count() != 0:
        warn_message = 'File already saved in {}.'.format(file_path)
        current_app.logger.warning(warn_message)
        flash(warn_message, category='warning')
        return

    filename_field.data.save(file_path)
    _create_thumbnail(file_path, thumbnail_path)
    current_app.logger.info('Thumbnail saved in: {}.'.format(thumbnail_path))

    picture_row_data = {
        'album_id': album_id,
        'uploader_id': current_user.id,
        'upload_date': datetime.now(),
        'path_to_image': file_path_web,
        'path_to_thumbnail': thumbnail_path_web,
        'name': name,
        'description': description
    }
    new_picture = Pictures(picture_row_data)
    db.session.add(new_picture)
    db.session.commit()

    flash("File " + file_name + " uploaded.", category='success')
