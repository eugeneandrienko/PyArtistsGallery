from flask import render_template, redirect, url_for, flash
from flask import request
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy.orm.exc import ObjectDeletedError

from pagapp import app
from pagapp import lm
from pagapp.forms import LoginForm, ChPasswdForm
from pagapp.forms import AddAlbumForm, EditAlbumForm, DeleteAlbumForm
from pagapp.forms import GotoUploadFakeForm
from pagapp.models import Users, Albums, Pictures


# List of views:
# User related:
#      /login
#      /chpasswd
#      /logout
#  Album-related:
#      /album/<albumurl>
#      /manage_albums
#  Picture-related:
#      /upload
#      /manage_pics  # TODO: incomplete!
#  Common:
#      /index
#      /


#
# User related views:
#  and one service function for Flask-Login
#

@lm.user_loader
def load_user(uid):
    try:
        result = Users.query.get(int(uid))
    except ObjectDeletedError:
        result = None
    return result


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        login_user(form.get_logged_in_user())
        return redirect(url_for('index'))
    elif form.login.data is not None or form.password.data is not None:
        flash('Login failed! Please double check your login name and password.')

    return render_template("login.html",
                           title=app.config['GALLERY_TITLE'],
                           form=form)


@app.route('/chpasswd', methods=['GET', 'POST'])
@login_required
def passwd():
    form = ChPasswdForm()

    if form.validate_on_submit():
        current_user.set_new_password(form.get_new_password())
        flash('Password successfully changed')
    elif (form.old_password.data is not None
          or form.new_password.data is not None
          or form.new_password2.data is not None
          ):
        # if some text entered in form, but we are here and not in
        # /index page -- login seems failed and we should show warning
        # message to user
        flash('Cannot change password - something goes wrong!')

    return render_template("passwd.html",
                           title=app.config['GALLERY_TITLE'],
                           form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


#
# Album-related views:
#

@app.route('/album/<albumurl>', methods=['GET', 'POST'])
def album(albumurl):
    fake_form = GotoUploadFakeForm()
    matched_album = Albums.query.filter_by(
        url_part=albumurl).first()
    if fake_form.validate_on_submit():
        return redirect(url_for('upload'))
    return render_template('album.html',
                           title=app.config['GALLERY_TITLE'],
                           album_name=matched_album.album_name,
                           album_description=matched_album.album_description,
                           albums=Albums.get_albums_list(),
                           pics=Pictures.query.filter_by(album_id=
                                                         matched_album.id),
                           fake_form=fake_form)


@app.route('/manage_albums', methods=['GET', 'POST'])
@login_required
def manage_albums():
    newalb_form = AddAlbumForm()
    editalb_form = EditAlbumForm()
    delalb_form = DeleteAlbumForm()
    editalb_form.album_select.choices = [('1', '1'), ('2', '2')]
    delalb_form.album_select.choices = [('1', '1'), ('2', '2')]

    if newalb_form.validate_on_submit():
        flash('Album ' + newalb_form.get_new_album_name() +
              ' successfully created.')
    elif newalb_form.get_new_album_name() is not None:
        flash("Cannot create album " +
              newalb_form.get_new_album_name() +
              ": it is already exists!")

    if editalb_form.validate_on_submit():
        if request.form['btn'] == 'Delete':
            print("Test passed")
        elif request.form['btn'] == 'Edit':
            print("Test passed #2")
    return render_template('manage_albums.html',
                           title=app.config['GALLERY_TITLE'],
                           newalb_form=newalb_form,
                           editalb_form=editalb_form,
                           delalb_form=delalb_form,
                           albums=Albums.get_albums_list())


#
# Picture-related views:
#

@app.route('/upload')
@login_required
def upload():
    return render_template('upload.html',
                           title=app.config['GALLERY_TITLE'])


#
# Common views and main view:
#

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    fake_form = GotoUploadFakeForm()
    if fake_form.validate_on_submit():
        return redirect(url_for('upload'))
    return render_template("index.html",
                           title=app.config['GALLERY_TITLE'],
                           albums=Albums.get_albums_list(),
                           fake_form=fake_form)