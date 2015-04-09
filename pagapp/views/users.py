from sqlalchemy.orm.exc import ObjectDeletedError
from flask import render_template, redirect, url_for, flash
from flask_login import logout_user, login_required

from pagapp import app
from pagapp import lm
from pagapp.forms import LoginForm, ChangePasswordForm
from pagapp.models import Users


@lm.user_loader
def load_user(uid):
    try:
        result = Users.query.get(int(uid))
    except ObjectDeletedError:
        result = None
    return result


@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()

    if login_form.validate_on_submit():
        return redirect(url_for('index'))
    elif (login_form.login.data is not None or
          login_form.password.data is not None):
        flash('Login failed! Please double check your login name and password.')

    return render_template(
        "login.html",
        title=app.config['GALLERY_TITLE'],
        form=login_form)


@app.route('/chpasswd', methods=['GET', 'POST'])
@login_required
def change_password():
    change_password_form = ChangePasswordForm()

    if change_password_form.validate_on_submit():
        flash('Password successfully changed')
    elif (change_password_form.old_password.data is not None
          or change_password_form.new_password.data is not None
          or change_password_form.new_password2.data is not None
          ):
        # If some text entered in change_password_form, but we are here
        # and not in /index page -- login seems failed and we should show
        # warning message to user.
        flash('Cannot change password - something goes wrong!')

    return render_template(
        "passwd.html",
        title=app.config['GALLERY_TITLE'],
        form=change_password_form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))