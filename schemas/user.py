from ma import ma
from models.user import UserModel, RoleEnum
from marshmallow import fields, validates, ValidationError


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserModel

    role = fields.Method("get_role_value", deserialize="load_role_enum")
    password = fields.Str(required=False)

    @validates("email")
    def validate_uniqueness_of_email(self, value):
        if UserModel.find_by_email(value):
            raise ValidationError(f"A user with email '{value}' already exists")

    def get_role_value(self, obj):
        return obj.role.value

    def load_role_enum(self, value):
        if not RoleEnum.has_role(value):
            raise ValidationError("Invalid role")
        else:
            return RoleEnum(value)


class UserRegisterSchema(UserSchema):
    password = fields.String(required=True)

    @validates("role")
    def user_cannot_register_a_role(self, _):
        raise ValidationError("Role is not allowed")
