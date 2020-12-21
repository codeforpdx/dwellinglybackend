from ma import ma
from models.property_assignment import PropertyAssignment
from models.user import UserModel, RoleEnum
from models.property import PropertyModel
from marshmallow import fields, validates, ValidationError


class PropertyAssignSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = PropertyAssignment
        include_fk = True
        relations = True

        propertyID = fields.Nested('PropertySchema')
        managerID = fields.Nested('UserSchema', required=True)


    @validates("manager_id")
    def validate_is_valid_user(self, value):
        if not UserModel.query.get(value):
            raise ValidationError('not a valid user id')

    @validates("property_id")
    def validate_is_valid_property(self, value):
        if not PropertyModel.query.get(value):
            raise ValidationError('not a valid property id')

    @validates("manager_id")
    def validate_role_property_manager(self, value):
        user = UserModel.query.get(value)
        if user.role != RoleEnum.PROPERTY_MANAGER:
            raise ValidationError('User is not a property manager')
