from pagapp import db


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True, nullable=False)
    password = db.Column(db.String(), index=True, unique=True, nullable=False)
    salt = db.Column(db.String(), index=True, nullable=False)

    def __init__(self, nickname, password, salt):
        self.nickname = nickname
        self.password = password
        self.salt = salt

    def __repr__(self):
        return 'Nickname: {}, pwd: {}, salt: {}'.format(
            self.nickname, self.password, self.salt)
