from db import db
from nobiru.nobiru_list import NobiruList
from queries.tenant_query import TenantQuery
from models.base_model import BaseModel
from models.tickets import TicketModel
from utils.time import Time
from models.lease import LeaseModel
from models.staff_tenant_link import StaffTenantLink


class TenantModel(BaseModel):
    __tablename__ = "tenants"

    query_class = TenantQuery

    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(100), nullable=False)
    lastName = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(40), nullable=False)
    archived = db.Column(db.Boolean, default=False, nullable=False)

    staff = db.relationship(
        "Staff",
        secondary=StaffTenantLink.tablename(),
        collection_class=NobiruList,
    )

    lease = db.relationship(
        LeaseModel,
        backref="tenant",
        cascade="all, delete-orphan",
        uselist=False,
    )

    tickets = db.relationship(
        TicketModel,
        backref="tenant",
        lazy=True,
        collection_class=NobiruList,
        cascade="all, delete-orphan",
    )

    def json(self):
        return {
            "id": self.id,
            "firstName": self.firstName,
            "lastName": self.lastName,
            "fullName": "{} {}".format(self.firstName, self.lastName),
            "phone": self.phone,
            "lease": self.lease.json() if self.lease else None,
            "staff": self.staff.json(),
            "created_at": Time.format_date(self.created_at),
            "updated_at": Time.format_date(self.updated_at),
            "archived": self.archived,
        }
