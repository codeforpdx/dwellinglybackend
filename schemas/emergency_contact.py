from ma import ma
from models.emergency_contact import EmergencyContactModel
from marshmallow import fields, validates, ValidationError

from schemas.contact_number import ContactNumberSchema


class EmergencyContactSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = EmergencyContactModel

    contact_numbers = fields.List(fields.Nested(ContactNumberSchema), required=True)

    @validates("name")
    def validates_uniqueness_of_name(self, value):
        if self.context.get("name") != value and EmergencyContactModel.find_by_name(
            value
        ):
            raise ValidationError(f"{value} is already an emergency contact")

    @validates("contact_numbers")
    def validate_contact_numbers(self, contact_numbers):
        if len(contact_numbers) < 1:
            raise ValidationError(
                "Emergency contacts must have at least one contact number."
            )
