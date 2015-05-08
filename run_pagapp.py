#!virtualenv/bin/python

from pagapp.create_pagapp import create_pagapp

app = create_pagapp('config')
app.run(debug=True)
