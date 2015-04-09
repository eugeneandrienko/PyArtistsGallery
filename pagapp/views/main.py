from flask import render_template, redirect, url_for

from pagapp import app
from pagapp.forms import AlbumForm
from pagapp.forms import GotoUploadFakeForm


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    album_form = AlbumForm()
    fake_form = GotoUploadFakeForm()

    if fake_form.validate_on_submit():
        return redirect(url_for('upload'))

    return render_template(
        "index.html",
        title=app.config['GALLERY_TITLE'],
        albums=album_form,
        fake_form=fake_form)