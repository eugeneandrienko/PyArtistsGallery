"""Functions, which help save uploaded files."""

from datetime import datetime
from flask import current_app, flash
from flask_login import current_user
from werkzeug.utils import secure_filename
from os.path import join

from pagapp.models import db
from pagapp.models.pictures import Pictures


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
    # TODO: create thumbnail here.
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
