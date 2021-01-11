from ma import ma
from models.emergency_contact import EmergencyContactModel
from utils.time import time_format
from marshmallow import fields, validates, ValidationError


class EmergencyContactSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = EmergencyContactModel

    created_at = fields.DateTime(time_format)
    updated_at = fields.DateTime(time_format)

    contact_numbers = fields.List(fields.Nested("ContactNumberSchema"), required=True)

    @validates("name")
    def validate_name(self, value):
        if EmergencyContactModel.find_by_name(value):
            raise ValidationError(f"{value} is already an emergency contact")

    @validates("contact_numbers")
    def validate_contact_numbers(self, contact_numbers):
        if len(contact_numbers) < 1:
            raise ValidationError(
                "Emergency contacts must have at least one contact number."
            )
