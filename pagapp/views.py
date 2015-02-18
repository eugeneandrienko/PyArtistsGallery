from flask import render_template
from pagapp import app
from .login_form import LoginForm


@app.route('/')
@app.route('/index')
def index():
    form = LoginForm()
    return render_template("index.html",
                           title="Test title",
                           form=form,
                           user_logged_in=False)
