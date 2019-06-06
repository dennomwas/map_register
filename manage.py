import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

# local imports
from map_api import create_app
from map_api.models import db

environment = os.getenv('FLASK_ENV', 'development')
app = create_app(environment)

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


if __name__ == "__main__":
    manager.run()
