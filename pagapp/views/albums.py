from flask import render_template, redirect, url_for, flash
from flask_login import login_required

from pagapp import app
from pagapp.forms.albums import AlbumForm, AddAlbumForm, EditAlbumForm, \
    DeleteAlbumForm
from pagapp.forms.pictures import PictureForm
from pagapp.forms.common import GotoUploadFakeForm


@app.route('/album/<albumurl>', methods=['GET', 'POST'])
def album(albumurl):
    fake_form = GotoUploadFakeForm()
    album_form = AlbumForm(albumurl)
    picture_form = PictureForm()

    if fake_form.validate_on_submit():
        return redirect(url_for('upload'))

    return render_template('album.html',
                           title=app.config['GALLERY_TITLE'],
                           album_name=album_form.get_matched_album().album_name,
                           album_description=album_form.get_matched_album(
                           ).album_description,
                           albums=album_form.get_album_list(),
                           pics=picture_form.get_pictures(
                               album_id=album_form.get_matched_album().id),
                           fake_form=fake_form)


@app.route('/manage_albums', methods=['GET', 'POST'])
@login_required
def manage_albums():
    alb_form = AlbumForm()
    newalb_form = AddAlbumForm()
    editalb_form = EditAlbumForm()
    delalb_form = DeleteAlbumForm()

    if newalb_form.validate_on_submit():
        flash('Album ' + newalb_form.get_new_album_name() +
              ' successfully created.')
    elif newalb_form.get_new_album_name() is not None:
        flash("Cannot create album " +
              newalb_form.get_new_album_name() +
              ": it is already exists!")

    if editalb_form.validate_on_submit():
        pass
    else:
        flash("")

    return render_template('manage_albums.html',
                           title=app.config['GALLERY_TITLE'],
                           newalb_form=newalb_form,
                           editalb_form=editalb_form,
                           delalb_form=delalb_form,
                           albums=alb_form.get_album_list())