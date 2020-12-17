from ma import ma
from models.property import PropertyModel
from marshmallow import fields, validates, ValidationError
from utils.time import time_format


class PropertySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = PropertyModel

    created_at = fields.DateTime(time_format)
    updated_at = fields.DateTime(time_format)
    propertyManagerIDs = fields.List(fields.Integer(), required=True)

    @validates("propertyManagerIDs")
    def validates_manager_assigned(self, value):
        if len(value) < 1:
            raise ValidationError('manager must be assigned')
