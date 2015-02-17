from flask import render_template
from pagapp import app


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html",
                           title="Test title")
