from sqlalchemy.orm import relationship
from db import db
from models.base_model import BaseModel
from models.tickets import TicketModel
from utils.time import Time


class TenantModel(BaseModel):
    __tablename__ = "tenants"

    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(100), nullable=False)
    lastName = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    archived = db.Column(db.Boolean, default=False, nullable=False)

    # relationships
    staff = relationship("UserModel", secondary="staff_tenant_links")
    leases = db.relationship("LeaseModel", backref="tenant", lazy=True)

    # BUG???
    # If I don't directly import - LINE 4 - I will get a SQL Error
    # sqlalchemy.exc.InvalidRequestError: When initializing mapper mapped class TenantModel->tenants, expression 'TicketModel' failed to locate a name ('TicketModel')
    # Staff and Leases relationship above doesn't seem to require a direct import though...
    # This causes an issue because TicketModel imports the TenantModel to get tenant name for its json output
    # If we directly import the TicketModel in this file - we will cause a circular import
    tickets = db.relationship("TicketModel", backref="tenant", lazy=True)

    # TODO: Do we add tickets to the json output?
    def json(self):
        return {
            "id": self.id,
            "firstName": self.firstName,
            "lastName": self.lastName,
            "fullName": "{} {}".format(self.firstName, self.lastName),
            "phone": self.phone,
            "lease": self.leases[0].json() if self.leases else "",
            "tickets": self.tickets,
            "staff": [user.json() for user in self.staff] if self.staff else [],
            "created_at": Time.format_date(self.created_at),
            "updated_at": Time.format_date(self.updated_at),
            "archived": self.archived,
        }
