from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# initialize SQLalchemy
db = SQLAlchemy()
marshmallow = Marshmallow()


class Base(db.Model):

    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime,  default=datetime.utcnow)
    date_modified = db.Column(db.DateTime,  default=datetime.utcnow,
                              onupdate=datetime.utcnow)


class User(Base):

    __tablename__ = 'users'

    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email_address = db.Column(db.String(100))
    password_hash = db.Column(db.String(50))

    def __repr__(self):
        return '<User: {}>'.format(self.firstname)


class MapRegister(Base):
    serial_no = db.Column(db.Integer)
