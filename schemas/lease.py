from ma import ma
from models.lease import LeaseModel
from models.tenant import TenantModel
from models.property import PropertyModel
from utils.time import time_format, iso_format
from marshmallow import fields, validates, ValidationError, post_load


class SharedLeaseValidations:
    propertyID = fields.Integer(required=True)
    dateTimeStart = fields.DateTime(iso_format, required=True)
    dateTimeEnd = fields.DateTime(iso_format, required=True)
    created_at = fields.DateTime(time_format)
    updated_at = fields.DateTime(time_format)

    @validates("propertyID")
    def validate_propertyID(self, value):
        if not PropertyModel.query.get(value):
            raise ValidationError(f"{value} is not a valid property ID")


class LeaseSchema(ma.SQLAlchemyAutoSchema, SharedLeaseValidations):
    class Meta:
        model = LeaseModel
        include_fk = True

    tenant = fields.Nested("TenantSchema")
    property = fields.Nested("PropertySchema")

    @validates("tenantID")
    def validate_tenantID(self, value):
        if not TenantModel.query.get(value):
            raise ValidationError(f"{value} is not a valid tenantID")


class BuildLeaseSchema(ma.SQLAlchemyAutoSchema, SharedLeaseValidations):
    class Meta:
        model = LeaseModel

    @post_load
    def make_lease(self, data, **kwargs):
        return LeaseModel(**data)
