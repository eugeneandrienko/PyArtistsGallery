from flask import render_template, redirect, url_for
from pagapp import app
from pagapp import lm
from pagapp.login_form import LoginForm
from flask.ext.login import login_user, logout_user
from pagapp.models import Users


@lm.user_loader
def load_user(id):
    try:
        result = Users.query.get(int(id))
    except:
        result = None
    return result


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        login_user(form.get_logged_in_user())
        return redirect(url_for('index'))

    return render_template("login.html",
                           title=app.config['GALLERY_TITLE'],
                           form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html",
                           title=app.config['GALLERY_TITLE'])
