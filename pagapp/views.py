from flask import render_template
from pagapp import app
from .login_form import LoginForm


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    user_logged_in = False
    form = LoginForm()

    if form.validate_on_submit():  # TODO: Add adequate user auth.
        if form.login.data == 'user' and form.password.data == 'qwerty':
            user_logged_in = True

    return render_template("index.html",
                           title="Test title",
                           form=form,
                           user_logged_in=user_logged_in)
