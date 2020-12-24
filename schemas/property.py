from ma import ma
from models.property import PropertyModel
from models.user import UserModel
from schemas.property_assignment import PropertyAssignSchema
from marshmallow import fields, validates, ValidationError, post_load
from utils.time import time_format


class PropertySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = PropertyModel

    created_at = fields.DateTime(time_format)
    updated_at = fields.DateTime(time_format)
    propertyManagerIDs = fields.List(fields.Integer(), required=True)

    @validates("propertyManagerIDs")
    def validates_property_manager_ids(self, value):
        if len(value) < 1:
            raise ValidationError('manager must be assigned')

        payload = [ {'manager_id': value[manager_id]} for manager_id in range(len(value)) ]
        PropertyModel.validate(PropertyAssignSchema, payload, partial=True, many=True)

    @validates("name")
    def validates_uniqueness_of_name(self, value):
        if PropertyModel.find_by_name(value):
            raise ValidationError('A property with this name already exists')

    @post_load
    def make_property_attributes(self, data, **kwargs):
        if 'propertyManagerIDs' in data:
            data['managers'] = [ UserModel.find(manager) for manager in data['propertyManagerIDs'] ]
            del(data['propertyManagerIDs'])
        return data
