from sqlalchemy.orm import relationship
from db import db
from models.base_model import BaseModel
from utils.time import Time
from models.lease import LeaseModel


class TenantModel(BaseModel):
    __tablename__ = "tenants"

    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(100), nullable=False)
    lastName = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    archived = db.Column(db.Boolean, default=False, nullable=False)

    # relationships
    staff = relationship("UserModel", secondary="staff_tenant_links")
    leases = db.relationship(
        "LeaseModel", backref="tenant", lazy="dynamic", cascade="all, delete-orphan"
    )

    def json(self):
        first_active_lease = self.leases.filter(LeaseModel.active()).first()
        active_lease_json = first_active_lease.json() if first_active_lease else ""
        return {
            "id": self.id,
            "firstName": self.firstName,
            "lastName": self.lastName,
            "fullName": "{} {}".format(self.firstName, self.lastName),
            "phone": self.phone,
            "lease": active_lease_json,
            "staff": [user.json() for user in self.staff] if self.staff else [],
            "created_at": Time.format_date(self.created_at),
            "updated_at": Time.format_date(self.updated_at),
            "archived": self.archived,
        }
