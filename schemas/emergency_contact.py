from ma import ma
from models.contact_number import ContactNumberModel
from models.emergency_contact import EmergencyContactModel
from schemas.contact_number import ContactNumberSchema
from utils.time import time_format
from marshmallow import fields, validates, ValidationError, EXCLUDE


class EmergencyContactSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = EmergencyContactModel

    created_at = fields.DateTime(time_format)
    updated_at = fields.DateTime(time_format)

    contact_numbers = fields.List(fields.Nested("ContactNumberSchema"))

    @validates("contact_numbers")
    def validate_contact_nums(self, value):
        print("validating contact_nums")
        try:
          self.contact_numbers = ContactNumberSchema(many=True).load(value)
        except ValidationError as err:
          self.contact_numbers = err.messages




    @validates("name")
    def validate_name(self, value):
        if EmergencyContactModel.find_by_name(value):
            raise ValidationError(f"{value} is already an emergency contact")


