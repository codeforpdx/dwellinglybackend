from ma import ma
from models.tenant import TenantModel
from marshmallow import fields, validate
from utils.time import time_format


class TenantSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TenantModel

    created_at = fields.DateTime(time_format)
    updated_at = fields.DateTime(time_format)

    firstName = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=100),
        error_messages={'required': 'First name is required.'},
    )

    lastName = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=100),
        error_messages={'required': 'Last name is required.'},
    )

    phone = fields.Str(
        required=True,
        validate=validate.Length(min=10, max=20),
        error_messages={'required': 'Phone number is required.'},
    )
