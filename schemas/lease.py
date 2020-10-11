from ma import ma
from models.lease import LeaseModel
from models.tenant import TenantModel
from models.property import PropertyModel
from schemas.time_format import time_format
from marshmallow import fields, validates, ValidationError


class LeaseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = LeaseModel
        include_fk = True

    dateTimeStart = fields.DateTime(time_format, required=True)
    dateTimeEnd = fields.DateTime(time_format, required=True)
    created_at = fields.DateTime(time_format)
    updated_at = fields.DateTime(time_format)

    @validates("tenantID")
    def validate_tenantID(self, value):
        if not TenantModel.query.get(value):
            raise ValidationError(f"{value} is not a valid tenant ID")

    @validates("propertyID")
    def validate_propertyID(self, value):
        if not PropertyModel.query.get(value):
            raise ValidationError(f"{value} is not a valid property ID")
