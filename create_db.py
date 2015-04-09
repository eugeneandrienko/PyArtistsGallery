#!bin/python

import hashlib
import uuid
import datetime

from pagapp import db
from pagapp.models import Users, Albums, Pictures


_USER = 'root'
_PASSWORD = 'toor'

db.create_all()
salt = uuid.uuid4().hex
hashed_pwd = hashlib.sha512(_PASSWORD.encode('utf-8') +
                            salt.encode('utf-8')).hexdigest()
admin_user = Users(_USER,
                   hashed_pwd,
                   salt,
                   True)
db.session.add(admin_user)

test_album = Albums('test_album',
                    'Test Album',
                    'This is a test album just for test')
db.session.add(test_album)
test_album = Albums('test_album2',
                    'Test Album 2',
                    'This is a test album #2 just for test #2')
db.session.add(test_album)

test_pic = Pictures(1, 1, datetime.datetime.now(), '/test.img',
                    '/test_thumb.img', 'Test Name')
db.session.add(test_pic)

db.session.commit()