"""Views for public part of application.

Anonymous user should be able to view next pages:
 * main page of application - implemented by index();
 * page with contents of selected album - implemented by album();
 * login page - implemented by login().
"""

from jinja2 import TemplateNotFound
from flask import render_template, abort, current_app
from flask import redirect, url_for, request, flash
from flask_login import login_user

from pagapp.models.albums import Albums
from pagapp.models.pictures import Pictures
from pagapp.models.users import Users
from pagapp.public_pages import public_pages
from pagapp.public_pages.forms import LoginForm
from pagapp.support_functions import flash_form_errors


@public_pages.route('/')
@public_pages.route('/index')
def index():
    """Renders main page of art gallery."""
    try:
        return render_template(
            'index.html',
            title=current_app.config['GALLERY_TITLE'],
            albums=Albums.get_albums_list())
    except TemplateNotFound:
        abort(404)

@public_pages.route('/album/<album_url>')
def album(album_url):
    """Renders page for album with given album's URL.

    Argument:
    album_url -- unique string, by which album can be accessed via web
    interface.
    """
    try:
        matched_album = Albums.query.filter_by(
            url_part=album_url).first()
        matched_pictures = Pictures.query.filter_by(
            album_id=matched_album.id)
    except AttributeError:
        flash('Album does not exists!', category='danger')
        return redirect(url_for('.index'))

    try:
        return render_template(
            'album.html',
            title=current_app.config['GALLERY_TITLE'],
            current_album=matched_album,
            albums=Albums.get_albums_list(),
            pictures=matched_pictures)
    except TemplateNotFound:
        abort(404)

@public_pages.route('/login', methods=['GET', 'POST'])
def login():
    """Renders login page.

    Function renders login page and raise messages for user if (s)he
    successfully logged in or not.
    """
    login_form = LoginForm(request.form)

    if request.method == 'POST' and login_form.validate():
        user = Users.query.filter_by(
            nickname=login_form.login.data).first()
        login_user(user)
        return redirect(url_for('admin_panel.panel'))
    else:
        flash_form_errors(login_form)

    try:
        return render_template(
            "login.html",
            title=current_app.config['GALLERY_TITLE'],
            form=login_form)
    except TemplateNotFound:
        abort(404)