from db import db
from models.base_model import BaseModel


class StaffTenantLink(BaseModel):
    __tablename__ = "staff_tenant_links"
    tenant_id = db.Column(db.Integer, db.ForeignKey("tenants.id"), primary_key=True)
    staff_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)

    # might want to set up relationships and backref's?
    # import from sqlalchemy.orm
    # something like:
    # tenant = relationship(TenantModel,
    #                       backref=backref('name', cascade='all, delete-orphan'))
