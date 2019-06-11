from map_api.models import marshmallow
from marshmallow import Schema, fields


class UserSchema(marshmallow.Schema):
    uuid = fields.String(dump_only=True)

    first_name = fields.String(required=True,
                               error_messages={'error': 'First Name cannot be blank'})

    last_name = fields.String(required=True,
                              error_messages={'error': 'Last Name cannot be blank'})

    email_address = fields.Email(required=True,
                                 error_messages={'error': 'Email cannot be blank'})

    date_created = fields.DateTime(dump_only=True)
    date_modified = fields.DateTime(dump_only=True)


class MapRegisterSchema(marshmallow.Schema):
    uuid = fields.String(dump_only=True)

    serial_no = fields.Integer(dump_only=True)

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
