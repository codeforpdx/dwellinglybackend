from ma import ma
from models.tickets import TicketModel
from models.tenant import TenantModel
from models.user import UserModel
from utils.time import time_format
from marshmallow import fields, validates, ValidationError


class TicketSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TicketModel
        include_fk = True

    tenant = fields.Nested("TenantSchema")
    user = fields.Nested("UserSchema")

    created_at = fields.DateTime(time_format)
    updated_at = fields.DateTime(time_format)

    @validates("tenantID")
    def validate_tenant(self, value):
        if not TenantModel.query.get(value):
            raise ValidationError(f"{value} is not a valid tenant ID")

    @validates("assignedUser")
    def validate_assigned_user(self, value):
        if not UserModel.query.get(value):
            raise ValidationError(f"{value} is not a valid user ID")

    @validates("sender")
    def validate_sender(self, value):
        if not UserModel.query.get(value):
            raise ValidationError(f"{value} is not a valid user ID")
