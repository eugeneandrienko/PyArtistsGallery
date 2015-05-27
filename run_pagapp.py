#!virtualenv/bin/python

from pagapp.create_pagapp import create_pagapp

app = create_pagapp('config.Config', debug=True)
app.run()
