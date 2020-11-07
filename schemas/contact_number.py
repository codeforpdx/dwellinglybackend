from ma import ma
from models.contact_number import ContactNumberModel
from utils.time import time_format
from marshmallow import fields, validates, ValidationError

class ContactNumberSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ContactNumberModel

    created_at = fields.DateTime(time_format)
    updated_at = fields.DateTime(time_format)
