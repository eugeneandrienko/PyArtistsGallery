# PyArtistsGallery

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

* `master` branch: [![Build Status](https://travis-ci.org/h0rr0rrdrag0n/PyArtistsGallery.svg?branch=master)](https://travis-ci.org/h0rr0rrdrag0n/PyArtistsGallery) [![Coverage Status](https://coveralls.io/repos/h0rr0rrdrag0n/PyArtistsGallery/badge.svg?branch=master)](https://coveralls.io/r/h0rr0rrdrag0n/PyArtistsGallery?branch=master) [![Code Health](https://landscape.io/github/h0rr0rrdrag0n/PyArtistsGallery/master/landscape.svg?style=flat)](https://landscape.io/github/h0rr0rrdrag0n/PyArtistsGallery/master)
* `develop` branch: [![Build Status](https://travis-ci.org/h0rr0rrdrag0n/PyArtistsGallery.svg?branch=develop)](https://travis-ci.org/h0rr0rrdrag0n/PyArtistsGallery) [![Coverage Status](https://coveralls.io/repos/h0rr0rrdrag0n/PyArtistsGallery/badge.svg?branch=develop)](https://coveralls.io/r/h0rr0rrdrag0n/PyArtistsGallery?branch=develop) [![Code Health](https://landscape.io/github/h0rr0rrdrag0n/PyArtistsGallery/develop/landscape.svg?style=flat)](https://landscape.io/github/h0rr0rrdrag0n/PyArtistsGallery/develop)

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
2. Clone this repository. After that create virtualenv (`virtualenv -p
python3.x .`), activate it (`source bin/activate`) and install all Python
requirements, described above (`pip install -r requirements.txt`).

### uWSGI

Execute uWSGI server with next command (virtualenv should be activated):
```
uwsgi --ini pagapp.ini
```

### Nginx

There is configuration for Nginx (assume, you cloned this repository to
the /usr/share/nginx/www/artgallery):
```
server {
    listen      8080;
    server_name "server.example";

    access_log /path/to/access.log;
    error_log  /path/to/error.log;

    location /static {
        alias /path/to/application/static;
    }

    location / {
        include uwsgi_params;
        uwsgi_pass unix:/tmp/uwsgi-pagapp.sock;
    }
}
```

After adding this configuration - do not forget to restart Nginx.
