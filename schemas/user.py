from ma import ma
from models.user import UserModel
from utils.time import time_format
from marshmallow import fields


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserModel

    created_at = fields.DateTime(time_format)
    updated_at = fields.DateTime(time_format)
