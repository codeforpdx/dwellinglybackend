from ma import ma
from models.property import PropertyModel
from .base_schema import BaseSchema

class PropertySchema(BaseSchema):
  class Meta:
    model = PropertyModel
