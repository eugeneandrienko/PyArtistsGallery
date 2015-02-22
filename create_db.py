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
db.session.commit()
