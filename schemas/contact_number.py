from ma import ma
from models.contact_number import ContactNumberModel
from utils.time import time_format
from marshmallow import fields, post_load, EXCLUDE


class ContactNumberSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ContactNumberModel
        unknown = EXCLUDE

    created_at = fields.DateTime(time_format)
    updated_at = fields.DateTime(time_format)

    @post_load
    def make_contact_nums(self, data, **kwargs):
        return ContactNumberModel(**data)

