import hashlib
import uuid
from pagapp import db


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True, nullable=False)
    password = db.Column(db.String(), index=True, unique=True, nullable=False)
    salt = db.Column(db.String(), index=True, nullable=False)
    active = db.Column(db.Boolean(), index=True)

    def __init__(self, nickname, password, salt, active):
        self.nickname = nickname
        self.password = password
        self.salt = salt
        self.active = active

    def __repr__(self):
        return 'Nickname: {}, pwd: {}, salt: {}'.format(
            self.nickname, self.password, self.salt)

    def is_authenticated(self):
        return True

    def is_active(self):
        return self.active

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def check_password(self, pwd):
        hashed_pwd = hashlib.sha512(
            pwd.encode('utf-8') + self.salt.encode('utf-8')).hexdigest()
        if hashed_pwd == self.password:
            return True
        else:
            return False

    def set_new_password(self, pwd):
        salt = uuid.uuid4().hex
        hashed_pwd = hashlib.sha512(
            pwd.encode('utf-8') + salt.encode('utf-8')).hexdigest()
        self.password = hashed_pwd
        self.salt = salt
        db.session.commit()


class Albums(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url_part = db.Column(db.String(), index=True, unique=True, nullable=False)
    album_name = db.Column(db.String(), index=True, unique=False, nullable=False)
    album_description = db.Column(db.String(), index=True, unique=False, nullable=True)

    def __init__(self, url_part, album_name, album_description):
        self.url_part = url_part
        self.album_name = album_name
        self.album_description = album_description

    def __repr__(self):
        return 'URL part: {}, Album: {}, Description: {}'.format(
            self.url_part,
            self.album_name,
            self.album_description)

    def get_albums_list(self):
        result = {}
        for album in self.query.all():
            result.update(
                {
                    'url_part': album.get_urlpart(),
                    'album_name': album.get_name(),
                    'album_description': self.get_description()
                 }
            )
        return result
