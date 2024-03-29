from map_api.models import marshmallow
from marshmallow import Schema, fields, ValidationError


class UserSchema(marshmallow.Schema):
    id = fields.String(dump_only=True)

    first_name = fields.String(required=True,
                               error_messages={'error': 'First Name cannot be blank'})

    last_name = fields.String(required=True,
                              error_messages={'error': 'Last Name cannot be blank'})

    email_address = fields.Email(required=True,
                                 error_messages={'error': 'Email cannot be blank'})

    password = fields.String(required=True,
                             error_messages={'error': 'Password cannot be blank'})

    date_created = fields.DateTime(dump_only=True)
    date_modified = fields.DateTime(dump_only=True)


class MapRegisterSchema(marshmallow.Schema):
    id = fields.String(dump_only=True)

    serial_no = fields.Integer(required=True,
                               error_messages={'error': 'Serial No. is required'})

    map_name = fields.String(required=True,
                             error_messages={'error': 'Map Name is required'})

    area = fields.String(required=True,
                         error_messages={'error': 'Area is required'})

    locality = fields.String(required=True,
                             error_messages={'error': 'Locality is required'})

    map_type = fields.String(required=True,
                             error_messages={'error': 'Map type is required'})

    lr_no = fields.String()

    fr_no = fields.String()

    sheet_no = fields.String()

    date_created = fields.DateTime()

    date_modified = fields.DateTime()

    created_by = fields.String()
