from flask import (Blueprint, g, request,
                   jsonify, json, render_template,
                   current_app, url_for)
from flask_restful import Api, Resource

# local imports
from map_api.models import User, auth, token_auth
from map_api.utils.schemas import UserSchema
from map_api.utils.email import send_mail
from config import Config

auth_blueprint = Blueprint('auth_blueprint', __name__)
auth_schema = UserSchema()
api = Api(auth_blueprint)


@auth.verify_password
def verify_user_password(email_address, password):

    user = User.query.filter_by(email_address=email_address).first()

    if not user or not user.verify_password(password):
        return False
    else:
        g.user = user
        return True


@token_auth.verify_token
def verify_user_token(token):
    user = User.verify_auth_token(token)

    if not user:
        return jsonify({'error': 'invalid'})
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

        if user and verify_user_password(email_address, password):

            token = user.generate_auth_token()
            return jsonify({'message': 'Logged in successfully!',
                            'token': token.decode('ascii')}, 201)
        else:
            return jsonify({'error': 'Email Address and Password do not match '}, 201)


class ResetPasswordLinkResource(Resource):

    def post(self):
        '''
        get user data
        check if valid
        check if it matches with an email in the db
        send link on email to reset password
        '''
        email_address = request.json.get('email_address')

        if email_address:
            user = User.query.filter_by(email_address=email_address).first()
            if not user:
                return jsonify({'error': 'Email does not exist'})

            token = user.generate_auth_token()
            reset_url = url_for('auth_blueprint.resetpassword',
                                token=token, _external=True)
            subject = "[Map Register] Password Reset Notification"
            html = render_template(
                'password_reset.html',
                user=user, reset_url=reset_url)

            send_mail(subject, Config.ADMINS[0], [email_address], html)
            return jsonify({'message': 'Check your Email/Spam Folder to reset the password'}, 200)

        return jsonify({'error': 'Please Check your fields and try again'}, 404)


class ResetPasswordResource(Resource):
    def post(self, token):
        '''
        verify token is valid
        check if user exists
        reset password
        '''
        email_address = request.json.get('email_address')
        password = request.json.get('password')

        if not email_address and not password:
            return jsonify({'error': 'Check your fields and try again'}, 404)

        user = User.query.filter_by(email_address=email_address).first()
        if user:
            token = request.args.get(token)
            validate_user = user.verify_auth_token(token)
            if not validate_user:
                return jsonify({'error': 'Operation not allowed'})

            new_password = User.set_password(password)
            new_password.save()

            return jsonify({'message': 'Password reset successfully'})

        return jsonify({'error': 'Email does not exist'})


class LogoutResource(AuthRequiredResource):
    def post(self):
        auth_header = request.headers.get('Authorization')
        print(auth_header, '\n\n\n\n')
        return auth_header


api.add_resource(RegistrationResource,
                 '/register',
                 '/register/',
                 endpoint='registration')

api.add_resource(LoginResource,
                 '/login',
                 '/login/',
                 endpoint='login')

api.add_resource(LogoutResource,
                 '/logout',
                 '/logout/',
                 endpoint='logout')

api.add_resource(ResetPasswordLinkResource,
                 '/reset-password-link',
                 '/reset-password-link/',
                 endpoint='resetpasswordlink')

api.add_resource(ResetPasswordResource,
                 '/reset-password',
                 '/reset-password/',
                 endpoint='resetpassword')
                 