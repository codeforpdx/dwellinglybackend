from ma import ma
from models.property import PropertyModel
from schemas.time_format import time_format
from marshmallow import fields

class PropertySchema(ma.SQLAlchemyAutoSchema):
  class Meta:
    model = PropertyModel
