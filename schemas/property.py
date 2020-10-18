from ma import ma
from models.property import PropertyModel

class PropertySchema(ma.SQLAlchemyAutoSchema):
  class Meta:
    model = PropertyModel
