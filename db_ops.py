from flask import Flask
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from pagapp.models import db
from pagapp.models.albums import Albums
from pagapp.models.configuration import Configuration
from pagapp.models.pictures import Pictures
from pagapp.models.users import Users
from pagapp.models.alembic_version import AlembicVersion


app = Flask(__name__)
app.config.from_object('config.Config')
db.init_app(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
