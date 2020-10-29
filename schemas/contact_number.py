from ma import ma
from models.contact_number import ContactNumberModel
from utils.time import time_format
from marshmallow import fields, validates, ValidationError

class ContactNumberSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ContactNumberModel
        include_fk = True

    created_at = fields.DateTime(time_format)
    updated_at = fields.DateTime(time_format)

    contact_number = fields.Nested("EmergencyContactSchema")

    @validates("number")
    @validates("contact_numbers")
    def validate_contact_numbers(self, value):
        if not ContactNumberModel.query.get(value):
            raise ValidationError(f"{value} is not a valid contact number")