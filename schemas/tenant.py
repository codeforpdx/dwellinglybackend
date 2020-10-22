from ma import ma
from models.tenant import TenantModel
from .base_schema import BaseSchema

class TenantSchema(BaseSchema):
  class Meta:
    model = TenantModel
