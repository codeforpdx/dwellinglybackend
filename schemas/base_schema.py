from ma import ma
from utils.time import time_format
from marshmallow import fields

# BaseSchema to inherit the common schema properties from
class BaseSchema(ma.SQLAlchemyAutoSchema):

  created_at = fields.DateTime(time_format)
  updated_at = fields.DateTime(time_format)
