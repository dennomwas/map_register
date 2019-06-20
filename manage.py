import os
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

# local imports
from map_api import create_app
from map_api.models import db, User, MapRegister

environment = os.getenv('FLASK_ENV', 'development')
app = create_app(environment)

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


def make_shell_context():
    return dict(app=app, db=db, User=User, MapRegister=MapRegister)


manager.add_command("shell", Shell(make_context=make_shell_context))

if __name__ == "__main__":
    manager.run()
