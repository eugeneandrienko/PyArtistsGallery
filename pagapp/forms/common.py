from flask_wtf import Form
from wtforms import SubmitField


# Fake form which using for redirect to /upload.
# Usual <a href="..." role="button" ...>...</a>
# do not work inside bootstrap's nav bar.
class GotoUploadFakeForm(Form):
    submit_button = SubmitField('Upload art')

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)