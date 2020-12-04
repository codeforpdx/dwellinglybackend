from db import db
from sqlalchemy.orm import relationship
from models.tenant import TenantModel
from models.user import UserModel
from models.base_model import BaseModel


class StaffTenantLink(BaseModel):
    __tablename__ = 'staff_tenant_links'
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenants.id'), primary_key=True)
    staff_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    tenant = relationship(TenantModel)
    staff = relationship(UserModel)

    # might want to set up relationships and backref's?
    # import from sqlalchemy.orm
    # something like:  tenant = relationship(TenantModel, backref=backref('name', cascade='all, delete-orphan')
