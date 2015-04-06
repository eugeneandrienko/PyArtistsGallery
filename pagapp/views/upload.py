from flask import render_template
from flask_login import login_required

from pagapp import app


@app.route('/upload')
@login_required
def upload():
    return render_template('upload.html',
                           title=app.config['GALLERY_TITLE'])