from ma import ma
from models.user import UserModel
from utils.time import time_format
from marshmallow import fields, validates, ValidationError


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserModel

    created_at = fields.DateTime(time_format)
    updated_at = fields.DateTime(time_format)

    @validates("email")
    def validate_uniqueness_of_email(self, value):
        if UserModel.find_by_email(value):
            raise ValidationError(f"A user with email '{value}' already exists")


class UserRegisterSchema(UserSchema):
    password = fields.String(required=True)

    @validates("role")
    def user_cannot_register_a_role(self, _):
        raise ValidationError("Role is not allowed")
