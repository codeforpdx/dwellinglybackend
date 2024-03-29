from ma import ma
from models.tenant import TenantModel
from models.users.staff import Staff
from marshmallow import fields, validate, validates, post_load
from utils.time import time_format
from schemas.staff_tenants import StaffTenantSchema


class TenantSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TenantModel

    created_at = fields.DateTime(time_format)
    updated_at = fields.DateTime(time_format)

    staffIDs = fields.List(fields.Integer(), required=False)
    lease = fields.Nested("BuildLeaseSchema")

    firstName = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=100),
        error_messages={"required": "First name is required."},
    )

    lastName = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=100),
        error_messages={"required": "Last name is required."},
    )

    phone = fields.Str(
        required=True,
        validate=validate.Length(min=10, max=30),
        error_messages={"required": "Phone number is required."},
    )

    archived = fields.Boolean(required=False)

    @validates("staffIDs")
    def validate_staff_ids(self, value):
        StaffTenantSchema().load({"staff": value}, partial=True)

    @post_load
    def make_tenant_attributes(self, data, **kwargs):
        if "staffIDs" in data:
            data["staff"] = [Staff.find(id) for id in data["staffIDs"]]
            del data["staffIDs"]
        return data
