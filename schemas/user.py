from ma import ma
from marshmallow import fields, validates, ValidationError, post_load

from models.user import UserModel, RoleEnum
from models.property import PropertyModel
from schemas.property_assignment import PropertyAssignmentSchema


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserModel

    role = fields.Method("get_role_value", deserialize="load_role_enum")
    type = fields.Str(required=False)
    password = fields.Str(required=False)

    @validates("email")
    def validate_uniqueness_of_email(self, value):
        if self.context.get("email") != value and UserModel.find_by_email(value):
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

    @validates("type")
    def user_cannot_register_a_type(self, _):
        raise ValidationError("Type is not allowed")


class PropertyManagerSchema(UserSchema):
    property_ids = fields.List(fields.Integer(), required=False)

    @validates("property_ids")
    def validate_property_ids(self, ids):
        for id in ids:
            PropertyAssignmentSchema().load({"property_id": id}, partial=True)

    @post_load
    def make_property_attributes(self, data, **kwargs):
        if "property_ids" in data:
            data["properties"] = [PropertyModel.find(id) for id in data["property_ids"]]
            del data["property_ids"]
        return data
