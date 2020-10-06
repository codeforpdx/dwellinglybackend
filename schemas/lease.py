from ma import ma
from models.lease import LeaseModel
from schemas.time_format import time_format
from marshmallow import fields


class LeaseSchema(ma.SQLAlchemyAutoSchema):
  class Meta:
    model = LeaseModel

  dateTimeStart = fields.DateTime(time_format)
  dateTimeEnd = fields.DateTime(time_format)
  dateUpdated = fields.DateTime(time_format)
  created_at = fields.DateTime(time_format)
  updated_at = fields.DateTime(time_format)
