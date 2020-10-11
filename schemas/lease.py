from ma import ma
from models.lease import LeaseModel
from schemas.time_format import time_format
from marshmallow import fields


class LeaseSchema(ma.SQLAlchemyAutoSchema):
  class Meta:
    model = LeaseModel
    include_fk = True

  dateTimeStart = fields.DateTime(time_format, required=True)
  dateTimeEnd = fields.DateTime(time_format, required=True)
  created_at = fields.DateTime(time_format)
  updated_at = fields.DateTime(time_format)
