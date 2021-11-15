from ma import ma
from marshmallow import validates, ValidationError

from models.property_assignment import PropertyAssignment
from models.users.property_manager import PropertyManager
from models.property import PropertyModel


class PropertyAssignmentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = PropertyAssignment
        include_fk = True

    @validates("property_id")
    def validate_is_valid_property(self, value):
        if not PropertyModel.query.get(value):
            raise ValidationError("not a valid property id")

    @validates("manager_id")
    def validate_role_property_manager(self, value):
        if not PropertyManager.query.get(value):
            raise ValidationError("User is not a property manager")
