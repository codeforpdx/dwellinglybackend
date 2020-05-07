from sqlalchemy.orm import relationship, backref
from db import db


class DepartmentEmployeeLink(db.Model):
    __tablename__ = "tenant_staff_link"
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenant.id'), primary_key=True)
    staff_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    tenant = relationship(db.Tenant, backref=backref("staff_assoc"))
    staff = relationship(db.Staff, backref=backref("tenant_assoc"))
