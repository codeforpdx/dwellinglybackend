from ma import ma
from models.tenant import TenantModel
from marshmallow import fields
from utils.time import time_format

class TenantSchema(ma.SQLAlchemyAutoSchema):
  class Meta:
    model = TenantModel

  addedOn = fields.DateTime(time_format)
  created_at = fields.DateTime(time_format)
  updated_at = fields.DateTime(time_format)
