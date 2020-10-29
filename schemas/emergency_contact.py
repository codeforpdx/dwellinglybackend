from ma import ma
from models.emergency_contact import EmergencyContactModel
from models.contact_number import ContactNumberModel
from utils.time import time_format
from marshmallow import fields, validates, ValidationError

class EmergencyContactSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = EmergencyContactModel
        include_fk = True

    created_at = fields.DateTime(time_format)
    updated_at = fields.DateTime(time_format)

    contact_number = fields.Nested("ContactNumberSchema")

# TODO: use same custom validation from ContactNumberSchema?
    @validates("contact_numbers")
    def validate_contact_numbers(self, value):
        if not ContactNumberModel.query.get(value):
            raise ValidationError(f"{value} is not a valid contact number")

# TODO: This should raise validation error when name is found? as it would not be unique?
    @validates("name")
    def validate_name(self, value):
        if not EmergencyContactModel.query.get(value):
            raise ValidationError(f"{value} is already an emergency contact")


