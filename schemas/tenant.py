from ma import ma
from models.tenant import TenantModel


class TenantSchema(ma.SQLAlchemyAutoSchema):
  class Meta:
    model = TenantModel
