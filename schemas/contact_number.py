from ma import ma
from models.contact_number import ContactNumberModel
from marshmallow import post_load, EXCLUDE


class ContactNumberSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ContactNumberModel
        unknown = EXCLUDE

    @post_load
    def make_contact_nums(self, data, **kwargs):
        return ContactNumberModel(**data)
