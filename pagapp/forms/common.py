"""Module for service forms

List of forms:
GotoUploadFakeForm -- service form, which redirects to /upload page.
"""

from flask_wtf import Form
from wtforms import SubmitField


class GotoUploadFakeForm(Form):
    """Fake service form for handling submit button presses.
    
    Fake form, which using for redirections to /upload.
    Usual <a href="..." role="button" ...>...</a> buttons
    do not work inside bootstrap's nav bar.
    """
    
    submit_button = SubmitField('Upload art')