from models.tenant import TenantModel
from models.users.staff import Staff
from marshmallow import Schema, fields, validates, ValidationError


class StaffTenantSchema(Schema):
    tenants = fields.List(fields.Int(), required=True)
    staff = fields.List(fields.Int(), required=True)

    @validates("tenants")
    def validate_tenant(self, value):
        if not len(value) > 0:
            raise ValidationError("At least one tenant ID is required")

        if not len(TenantModel.query.filter(TenantModel.id.in_(value)).all()) == len(
            value
        ):
            raise ValidationError(f"{value} contains invalid tenant IDs")

    @validates("staff")
    def validate_staff(self, value):
        if not len(Staff.query.filter(Staff.id.in_(value)).all()) == len(value):
            raise ValidationError(f"{value} contains invalid staff IDs")
