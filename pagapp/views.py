from flask import render_template
from pagapp import app, models
from .login_form import LoginForm
import hashlib


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    user_logged_in = False
    form = LoginForm()

    users = models.Users.query.all()
    if form.validate_on_submit():
        for user in users:
            hashed_pwd = hashlib.sha512(
                form.password.data.encode('utf-8') +
                user.salt.encode('utf-8')).hexdigest()
            if hashed_pwd == user.password:
                user_logged_in = True
                break

    return render_template("index.html",
                           title=app.config['GALLERY_TITLE'],
                           form=form,
                           user_logged_in=user_logged_in)
