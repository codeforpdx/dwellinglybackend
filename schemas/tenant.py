from ma import ma
from models.tenant import TenantModel
from schemas.time_format import time_format
from marshmallow import fields


class TenantSchema(ma.SQLAlchemyAutoSchema):
  class Meta:
    model = TenantModel

  addedOn = fields.DateTime(time_format)
  created_at = fields.DateTime(time_format)
  updated_at = fields.DateTime(time_format)
