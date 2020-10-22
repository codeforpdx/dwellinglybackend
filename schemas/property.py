from ma import ma
from models.property import PropertyModel
from marshmallow import fields
from utils.time import time_format

class PropertySchema(ma.SQLAlchemyAutoSchema):
  class Meta:
    model = PropertyModel

  created_at = fields.DateTime(time_format)
  updated_at = fields.DateTime(time_format)
