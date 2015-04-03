from flask_wtf import Form


# Fake form which using for redirect to /upload.
# Usual <a href="..." role="button" ...>...</a>
# do not work inside bootstrap's nav bar.
class GotoUploadFakeForm(Form):
    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)