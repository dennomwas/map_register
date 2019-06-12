from flask import Blueprint, g, request, jsonify, json
from flask_restful import Api, Resource

# local imports
from map_api.models import User, auth, token_auth
from map_api.utils.schemas import UserSchema

auth_blueprint = Blueprint('auth_blueprint', __name__)
auth_schema = UserSchema()
api = Api(auth_blueprint)


@auth.verify_password
def verify_user_password(email_address, password):

    user = User.query.filter_by(email_address=email_address).first()
    print(user, '\n\n\n\n\n')
    if not user or not user.verify_password(password):
        return False
    else:
        g.user = user
        return True


@token_auth.verify_token
def verify_user_token(token):
    user = User.verify_auth_token(token)

    if not user:
        return False
    else:
        g.user = user
        return True


class AuthRequiredResource(Resource):
    method_decorators = [token_auth.login_required]


class RegistrationResource(Resource):
    def post(self):
        '''
        get user data
        validate errors using schemas
        check if user exists - matching emails
        add user to db
        rollback if errors
        '''

        payload = request.get_json(silent=True)

        errors = auth_schema.validate(payload)
        if errors:
            return jsonify(errors=errors, status=404)

        email_address = payload.get('email_address')
        user = User.query.filter_by(email_address=email_address).first()
        if not user:
            user = User(
                first_name=payload['first_name'],
                last_name=payload['last_name'],
                email_address=payload['email_address'],
                password=payload['password']
            )
            user.save()
            return jsonify({'message': 'User successfully added'}, 201)
        else:
            return jsonify({'error': 'Username already exists'}, 404)


class LoginResource(Resource):
    def post(self):
        '''
        get user data
        check if data is valid
        check if user exists in db
        check is passwords match
        login user/generate token
        '''
        email_address = request.json.get('email_address')
        password = request.json.get('password')

        if not email_address or not password:
            return jsonify({'error': 'Check your Email Address/Password and try again'}, 201)

        user = User.query.filter_by(email_address=email_address).first()

        if user and verify_user_password(user.email_address, password):

            token = user.generate_auth_token()
            return jsonify({'message': 'Logged in successfully!',
                            'token': token.decode('ascii')}, 201)
        else:
            return jsonify({'error': 'Check your Email Address/Password and try again'}, 201)

api.add_resource(RegistrationResource, '/register', endpoint='registration')
api.add_resource(LoginResource, '/login', endpoint='login')
