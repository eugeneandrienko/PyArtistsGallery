#!bin/python

from pagapp import db, models
import hashlib
import uuid

USER = 'root'
PASSWORD = 'toor'

db.create_all()
salt = uuid.uuid4().hex
hashed_pwd = hashlib.sha512(PASSWORD.encode('utf-8') + salt.encode('utf-8')).hexdigest()
admin_user = models.Users(USER,
                          hashed_pwd,
                          salt,
                          True)
db.session.add(admin_user)

test_album = models.Albums('test_album',
                           'Test Album',
                           'This is a test album just for test')
db.session.add(test_album)
test_album = models.Albums('test_album2',
                           'Test Album 2',
                           'This is a test album #2 just for test #2')
db.session.add(test_album)

db.session.commit()
