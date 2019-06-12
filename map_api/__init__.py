from flask import Flask

# local imports
from map_api.models import db
from config import app_config




def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    try:
        app.config.from_pyfile('config.py', silent=False)
    except FileNotFoundError:
        pass

    db.init_app(app)

    from map_api.map_auth.views import auth_blueprint
    from map_api.map_views.views import map_blueprint

    app.register_blueprint(auth_blueprint, url_prefix='/v1/auth')
    app.register_blueprint(map_blueprint, url_prefix='/v1/map-register')

    return app
