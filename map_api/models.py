import uuid
from datetime import datetime
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from flask_marshmallow import Marshmallow
from sqlalchemy.orm import relationship
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import ForeignKey, Column
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer,
                          BadSignature, SignatureExpired)

# local imports
from config import Config

# initialize SQLalchemy
db = SQLAlchemy()
marshmallow = Marshmallow()
auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()


def generate_uuid():
    return str(uuid.uuid4())


class Base(db.Model):

    __abstract__ = True

    id = db.Column(db.String, primary_key=True, default=generate_uuid)
    date_created = db.Column(db.DateTime,  default=datetime.utcnow)
    date_modified = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def save(self):
        ''' Save an object to database '''
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except SQLAlchemyError as error:
            db.session.rollback()
            return False

    def update(self):
        ''' Update an existing object in the database '''
        try:
            db.session.commit()
            return True
        except SQLAlchemyError as error:
            db.session.rollback()
            return False

    def delete(self):
        ''' delete an object from the database '''
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except SQLAlchemyError as error:
            db.session.rollback()
            return False


class User(Base):

    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email_address = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(), nullable=False)
    map = db.relationship("MapRegister",
                          backref="users",
                          lazy='dynamic')

    @property
    def password(self):
        """ Prevent password from being accessed """

        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        """ Sets a hashed password """

        self.password_hash = generate_password_hash(password)

    def set_password(self, password):
        """ Set password to a hashed password """

        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """ Check hashed password matches actual password """

        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self, expiration=3600):
        serializer = Serializer(Config.SECRET_KEY, expires_in=expiration)
        return serializer.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        serializer = Serializer(Config.SECRET_KEY)
        try:
            data = serializer.loads(token)

        except SignatureExpired:
            return jsonify(None, {'error': 'Expired Token, Login Again'})

        except BadSignature:
            return jsonify(None, {'error': 'Invalid Token, Login Again'})

        user = User.query.get(data['id'])
        return user

    def __repr__(self):
        return '<User: {}>'.format(self.first_name)


class MapRegister(Base):

    __tablename__ = 'map_register'

    serial_no = db.Column(db.Integer(), nullable=False, autoincrement=True)
    map_name = db.Column(db.String(100), nullable=False)
    area = db.Column(db.String(100), nullable=False)
    locality = db.Column(db.String(100), nullable=False)
    map_type = db.Column(db.String(100), nullable=False)
    lr_no = db.Column(db.String(100))
    fr_no = db.Column(db.String(100))
    sheet_no = db.Column(db.String(100))

    created_by = db.Column(db.String,
                           db.ForeignKey('users.id'),
                           nullable=False)
    # modified_by = db.Column(db.String,
    #                         db.ForeignKey('users.id'),
    #                         nullable=True)

    def __repr__(self):
        return '<MapRegister: {}>'.format(self.map_name)
