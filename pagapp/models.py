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

    def get_url_part(self):
        return self.url_part

    def get_album_name(self):
        return self.album_name

    def get_album_description(self):
        return self.album_description

    def __init__(self, url_part, album_name, album_description):
        self.url_part = url_part
        self.album_name = album_name
        self.album_description = album_description

    def __repr__(self):
        return 'URL part: {}, Album: {}, Description: {}'.format(
            self.url_part,
            self.album_name,
            self.album_description)

    @classmethod
    def get_albums_list(cls):
        result = []
        for album in cls.query.all():
            result.append(
                {
                    'url_part': album.get_url_part(),
                    'album_name': album.get_album_name(),
                    'album_description': album.get_album_description()
                }
            )
        return result


class Pictures(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    album_id = db.Column(db.Integer, db.ForeignKey('albums.id'))
    path_to_image = db.Column(db.String(), index=True, nullable=False)
    path_to_thumb = db.Column(db.String(), index=True, nullable=False)
    name = db.Column(db.String(), index=True, nullable=False)
    upload_date = db.Column(db.DateTime(), index=True, nullable=False)
    uploader_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, album_id, uploader_id, upload_date, path_to_image, path_to_thumb, name=''):
        self.album_id = album_id
        self.path_to_image = path_to_image
        self.path_to_thumb = path_to_thumb
        self.name = name
        self.upload_date = upload_date
        self.uploader_id = uploader_id

    def __repr__(self):
        return 'Album ID: {}, Uploader ID: {}, Date: {}, Path: {}|{}, Name: {}'.format(
            str(self.album_id), str(self.uploader_id),
            str(self.upload_date),
            self.path_to_image,
            self.path_to_thumb,
            self.name)
