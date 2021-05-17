from db import db
from utils.nobiru import NobiruList
from models.base_model import BaseModel
from models.tickets import TicketModel
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
    staff = db.relationship(
        "UserModel",
        secondary="staff_tenant_links",
        backref="tenants",
        collection_class=NobiruList,
    )
    leases = db.relationship(
        "LeaseModel",
        backref="tenant",
        lazy="dynamic",
        cascade="all, delete-orphan",
        collection_class=NobiruList,
    )
    tickets = db.relationship(
        TicketModel, backref="tenant", lazy=True, collection_class=NobiruList
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
            "staff": self.staff.json(),
            "created_at": Time.format_date(self.created_at),
            "updated_at": Time.format_date(self.updated_at),
            "archived": self.archived,
        }
