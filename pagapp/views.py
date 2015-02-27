from flask import render_template, redirect, url_for, flash
from pagapp import app
from pagapp import lm
from pagapp.login_form import LoginForm
from pagapp.passwd_form import PasswdForm
from flask.ext.login import login_user, logout_user, login_required, current_user
from pagapp.models import Users


@lm.user_loader
def load_user(id):
    try:
        result = Users.query.get(int(id))
    except:
        result = None
    return result


@app.route('/passwd', methods=['GET', 'POST'])
@login_required
def passwd():
    form = PasswdForm()

    if form.validate_on_submit():
        current_user.set_new_password(form.get_new_password())
        flash('Password successfully changed')
    elif form.old_password.data is not None \
        or form.new_password.data is not None \
        or form.new_password2.data is not None:
        # if some text entered in form, but we are here and not in
        # /index page -- login seems failed and we should show warning
        # message to user
        flash('Cannot change password - something goes wrong!')

    return render_template("passwd.html",
                           title=app.config['GALLERY_TITLE'],
                           form=form)


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


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html",
                           title=app.config['GALLERY_TITLE'])
