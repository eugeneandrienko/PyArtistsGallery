from flask import render_template, redirect, url_for, flash
from flask_login import login_required

from pagapp import app
from pagapp.forms import AlbumForm, AddAlbumForm, \
    EditAlbumNameForm, EditAlbumDescForm, DeleteAlbumForm
from pagapp.forms import PictureForm
from pagapp.forms import GotoUploadFakeForm


@app.route('/album/<album_url>', methods=['GET', 'POST'])
def album(album_url):
    fake_form = GotoUploadFakeForm()
    album_form = AlbumForm(album_url)
    picture_form = PictureForm()

    if fake_form.validate_on_submit():
        return redirect(url_for('upload'))

    return render_template(
        'album.html',
        title=app.config['GALLERY_TITLE'],
        album_name=album_form.matched_album.album_name,
        album_description=album_form.matched_album.album_description,
        albums=album_form.get_albums_list(),
        pics=picture_form.get_pictures(
            album_id=album_form.matched_album.id),
        fake_form=fake_form)


@app.route('/manage_albums', methods=['GET', 'POST'])
@login_required
def manage_albums():
    new_album_form = AddAlbumForm(prefix='new_album_form')
    edit_album_name_form = EditAlbumNameForm(prefix='edit_album_name_form')
    edit_album_description_form = EditAlbumDescForm(
        prefix='edit_album_description_form')
    delete_album_form = DeleteAlbumForm(prefix='delete_album_form')

    if new_album_form.submit_button.data is True:
        if new_album_form.validate():
            flash('Album ' +
                  new_album_form.new_album.data +
                  ' successfully created.')
            edit_album_name_form.update_select_choices()
            edit_album_description_form.update_select_choices()
            delete_album_form.update_select_choices()
        else:
            flash("Cannot create album " +
                  new_album_form.new_album.data +
                  ": it is already exists!")

    if edit_album_name_form.submit_button.data is True:
        if edit_album_name_form.validate():
            flash("Album " +
                  edit_album_name_form.album_select.data +
                  " renamed to " +
                  edit_album_name_form.album_name.data)
            edit_album_description_form.update_select_choices()
            delete_album_form.update_select_choices()
        else:
            flash("Cannot rename " +
                  edit_album_name_form.album_select.data +
                  " !")

    if edit_album_description_form.submit_button.data is True:
        if edit_album_description_form.validate():
            flash("Album " +
                  edit_album_description_form.album_select.data +
                  " successfully edited")
            edit_album_name_form.update_select_choices()
            delete_album_form.update_select_choices()
        else:
            flash("Cannot save " +
                  edit_album_description_form.album_select.data +
                  " album!")

    if delete_album_form.submit_button.data is True:
        if delete_album_form.validate():
            flash("Album " +
                  delete_album_form.album_select.data +
                  " successfully deleted")
            edit_album_name_form.update_select_choices()
            edit_album_description_form.update_select_choices()
        else:
            flash("Cannot delete album " +
                  delete_album_form.album_select.data +
                  "!")

    album_form = AlbumForm()

    return render_template(
        'manage_albums.html',
        title=app.config['GALLERY_TITLE'],
        newalb_form=new_album_form,
        editalbname_form=edit_album_name_form,
        editalbdesc_form=edit_album_description_form,
        delalb_form=delete_album_form,
        albums=album_form)