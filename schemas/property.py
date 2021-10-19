from ma import ma
from models.property import PropertyModel
from models.users.property_manager import PropertyManager
from schemas.property_assignment import PropertyAssignSchema
from marshmallow import fields, validates, ValidationError, post_load
from utils.time import time_format
from tests.helpers.matchers import blank


class PropertySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = PropertyModel

    created_at = fields.DateTime(time_format)
    updated_at = fields.DateTime(time_format)
    propertyManagerIDs = fields.List(fields.Integer(), required=True)

    @validates("propertyManagerIDs")
    def validates_property_manager_ids(self, value):
        if len(value) < 1:
            raise ValidationError("manager must be assigned")

        payload = [
            {"manager_id": value[manager_id]} for manager_id in range(len(value))
        ]
        PropertyAssignSchema().load(payload, partial=True, many=True)

    @validates("name")
    def validates_uniqueness_of_name(self, value):
        def _assigning_name():
            if "name" in self.context and value == self.context["name"]:
                return False
            return True

        if _assigning_name() and PropertyModel.find_by_name(value):
            raise ValidationError("A property with this name already exists")
        if blank(value):
            raise ValidationError("Property name cannot be blank")

    @post_load
    def make_property_attributes(self, data, **kwargs):
        if "propertyManagerIDs" in data:
            data["managers"] = [
                PropertyManager.find(id) for id in data["propertyManagerIDs"]
            ]
            del data["propertyManagerIDs"]
        return data
