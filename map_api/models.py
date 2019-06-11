import uuid
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey, Column
from flask_marshmallow import Marshmallow
from werkzeug.security import generate_password_hash, check_password_hash

# initialize SQLalchemy
db = SQLAlchemy()
marshmallow = Marshmallow()
auth = HTTPBasicAuth()


def generate_uuid():
    return str(uuid.uuid4())


class Base(db.Model):

    __abstract__ = True

    uuid = db.Column(db.String, primary_key=True, default=generate_uuid)
    date_created = db.Column(db.DateTime,  default=datetime.utcnow)
    date_modified = db.Column(db.DateTime,  default=datetime.utcnow,
                              onupdate=datetime.utcnow)


class User(Base):

    __tablename__ = 'users'

    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email_address = db.Column(db.String(100))
    password_hash = db.Column(db.String(50))
    map = db.relationship("MapRegister",
                          back_populates="users",
                          lazy='dynamic')

    def __repr__(self):
        return '<User: {}>'.format(self.firstname)

    @property
    def password(self):
        """ Prevent password from being accessed """

        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        """ Sets a hashed password """

        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """ Check hashed password matches actual password """

        return check_password_hash(self.password_hash, password)

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
    user = db.relationship("User",
                           back_populates="map_register",
                           lazy='dynamic')
    created_by = db.Column(db.String,
                           db.ForeignKey('users.uuid'),
                           nullable=False)

    def __repr__(self):
        return '<MapRegister: {}>'.format(self.map_name)
