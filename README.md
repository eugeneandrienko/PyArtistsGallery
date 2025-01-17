__Repository moved to https://codeberg.org/evgandr/PyArtistsGallery__

# PyArtistsGallery

[![PyPI](https://img.shields.io/pypi/v/PyArtistsGallery.svg)](https://pypi.python.org/pypi/PyArtistsGallery/) [![PyPI](https://img.shields.io/pypi/status/PyArtistsGallery.svg)]() [![PyPI](https://img.shields.io/pypi/pyversions/PyArtistsGallery.svg)]() [![PyPI](https://img.shields.io/pypi/l/PyArtistsGallery.svg)]()

## About PyArtistsGallery

There is standalone web-gallery for arts and photos. Based on Python 3, Flask
and SQLite.

I have searched for small standalone web-gallery without big monsters like
MySQL in dependencies (because I cannot run MySQL in my RaspberryPi without
liters of liquid nitrogen). I found bunch of galleries, like sfpg
(https://sye.dk/sfpg/), but they looks not so nice for me or generate
thumbnails for new pictures then user tries to load main page of gallery.

That's why I wrote my own gallery, which looks like I want and do what I want.

## Repository status:

* `master` branch:  [![Build Status](https://travis-ci.org/h0rr0rrdrag0n/PyArtistsGallery.svg?branch=master)](https://travis-ci.org/h0rr0rrdrag0n/PyArtistsGallery) [![Coverage Status](https://coveralls.io/repos/h0rr0rrdrag0n/PyArtistsGallery/badge.svg?branch=master)](https://coveralls.io/r/h0rr0rrdrag0n/PyArtistsGallery?branch=master) [![Code Health](https://landscape.io/github/h0rr0rrdrag0n/PyArtistsGallery/master/landscape.svg?style=flat)](https://landscape.io/github/h0rr0rrdrag0n/PyArtistsGallery/master) [![Requirements Status](https://requires.io/github/h0rr0rrdrag0n/PyArtistsGallery/requirements.svg?branch=master)](https://requires.io/github/h0rr0rrdrag0n/PyArtistsGallery/requirements/?branch=master)
* `develop` branch: [![Build Status](https://travis-ci.org/h0rr0rrdrag0n/PyArtistsGallery.svg?branch=develop)](https://travis-ci.org/h0rr0rrdrag0n/PyArtistsGallery) [![Coverage Status](https://coveralls.io/repos/h0rr0rrdrag0n/PyArtistsGallery/badge.svg?branch=develop)](https://coveralls.io/r/h0rr0rrdrag0n/PyArtistsGallery?branch=develop) [![Code Health](https://landscape.io/github/h0rr0rrdrag0n/PyArtistsGallery/develop/landscape.svg?style=flat)](https://landscape.io/github/h0rr0rrdrag0n/PyArtistsGallery/develop) [![Requirements Status](https://requires.io/github/h0rr0rrdrag0n/PyArtistsGallery/requirements.svg?branch=develop)](https://requires.io/github/h0rr0rrdrag0n/PyArtistsGallery/requirements/?branch=develop)

## Requirements

* Python 3.3+
* Pillow
  - python3-dev
  - libjpeg-dev
  - zlib1g-dev
* flask
* flask-wtf
* flask-sqlalchemy
* flask-login
* flask-migrate
* flask-script
* uWSGI

Install requirements for Pillow _before_ you install pip and virtualenv
as described below.

## Installation

1. Install pip and virtualenv.
2. Create virtualenv (`virtualenv -p python3.x .`), and activate it (`source
bin/activate`).
3. Install PyArtistsGallery via `pip install PyArtistsGallery`. Application
will be installed in the `virtualenv/lib/python3.x/site-packages`. I will
refer to this path as `/path/to/site-packages/`

### uWSGI

Execute uWSGI server with next command (virtualenv should be activated):
```
uwsgi --ini /path/to/site-packages/pagapp.ini
```

### Nginx

There is configuration for Nginx (assume, you cloned this repository to
the /usr/share/nginx/www/artgallery):
```
server {
    listen      8080;
    server_name "server.example";
    client_max_body_size 50M;

    access_log /path/to/access.log;
    error_log  /path/to/error.log;

    location /static {
        alias /path/to/site-packages/static;
    }

    location / {
        include uwsgi_params;
        uwsgi_pass unix:/tmp/uwsgi-pagapp.sock;
    }
}
```

After adding this configuration - do not forget to restart Nginx.
