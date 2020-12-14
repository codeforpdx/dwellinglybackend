from ma import ma
from models.tenant import TenantModel
from models.user import UserModel, RoleEnum
from utils.time import time_format
from marshmallow import Schema, fields, validates, ValidationError


class StaffTenantSchema(Schema):
    tenants = fields.List(fields.Int(), required=True)
    staff = fields.List(fields.Int(), required=True)
    created_at = fields.DateTime(time_format)
    updated_at = fields.DateTime(time_format)

    @validates("tenants")
    def validate_tenant(self, value):
        if not len(value) > 0:
            raise ValidationError("At least one tenant ID is required")

        if not len(TenantModel.query.filter(TenantModel.id.in_(value)).all()) == len(value):
            raise ValidationError(f"{value} contains invalid tenant IDs")

    @validates("staff")
    def validate_staff(self, value):
        staff_query = UserModel.query.filter(
            UserModel.id.in_(value),
            UserModel.role == RoleEnum.STAFF
        )

        if not len(staff_query.all()) == len(value):
            raise ValidationError(f"{value} contains invalid staff IDs")
