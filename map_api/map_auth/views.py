from flask import Blueprint, g
from flask_restful import Api, Resource

# local imports
from map_api.models import User
from map_api.utils.schemas import UserSchema

auth_blueprint = Blueprint('auth_blueprint', __name__)
auth_schema = UserSchema()
api = Api(auth_blueprint)

class RegistrationResource(Resource):
    def post(self):
        x = 'register here'
        return x

class LoginResource(Resource):
    def post(self):
        pass

api.add_resource(RegistrationResource, '/register', endpoint='registration')
api.add_resource(LoginResource, '/login', endpoint='login')
