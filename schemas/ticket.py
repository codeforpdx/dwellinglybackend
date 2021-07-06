from ma import ma
from models.tickets import TicketModel
from models.tenant import TenantModel
from models.user import UserModel
from marshmallow import fields, validates, ValidationError


class TicketSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TicketModel
        include_fk = True

    tenant = fields.Nested("TenantSchema")
    author = fields.Nested("UserSchema")

    @validates("tenant_id")
    def validate_tenant(self, value):
        if not TenantModel.query.get(value):
            raise ValidationError(f"{value} is not a valid tenant ID")

    @validates("author_id")
    def validate_author(self, value):
        if not UserModel.query.get(value):
            raise ValidationError(f"{value} is not a valid user ID")
