from flask import render_template, redirect, url_for, flash
from flask_login import login_required

from pagapp import app
from pagapp.forms.albums import AlbumForm, AddAlbumForm, \
    EditAlbumNameForm, EditAlbumDescForm, DeleteAlbumForm
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
    newalb_form = AddAlbumForm(prefix='newalb_form')
    editalbname_form = EditAlbumNameForm(prefix='editalbname_form')
    editalbdesc_form = EditAlbumDescForm(prefix='editalbdesc_form')
    delalb_form = DeleteAlbumForm(prefix='delalb_form')

    if newalb_form.submit_button.data is True:
        if newalb_form.validate():
            flash('Album ' +
                  newalb_form.get_new_album_name() +
                  ' successfully created.')
            editalbname_form.update_select_choices()
            editalbdesc_form.update_select_choices()
            delalb_form.update_select_choices()
        else:
            flash("Cannot create album " +
                  newalb_form.get_new_album_name() +
                  ": it is already exists!")

    if editalbname_form.submit_button.data is True:
        if editalbname_form.validate():
            flash("Album " +
                  editalbname_form.get_old_album_name() +
                  " renamed to " +
                  editalbname_form.get_album_name())
            editalbdesc_form.update_select_choices()
            delalb_form.update_select_choices()
        else:
            flash("Cannot rename " +
                  editalbname_form.get_old_album_name() +
                  " !")

    if editalbdesc_form.submit_button.data is True:
        if editalbdesc_form.validate():
            flash("Album " +
                  editalbdesc_form.get_album_name() +
                  " successfully edited")
            editalbname_form.update_select_choices()
            delalb_form.update_select_choices()
        else:
            flash("Cannot save " +
                  editalbdesc_form.get_album_name() +
                  " album!")

    if delalb_form.submit_button.data is True:
        if delalb_form.validate():
            flash("Album " +
                  delalb_form.get_album_name() +
                  " successfully deleted")
            editalbname_form.update_select_choices()
            editalbdesc_form.update_select_choices()
        else:
            flash("Cannot delete album " +
                  delalb_form.get_album_name() +
                  "!")

    alb_form = AlbumForm()

    return render_template('manage_albums.html',
                           title=app.config['GALLERY_TITLE'],
                           newalb_form=newalb_form,
                           editalbname_form=editalbname_form,
                           editalbdesc_form=editalbdesc_form,
                           delalb_form=delalb_form,
                           albums=alb_form.get_album_list())