from db import db
from utils.time import Time

from models.base_model import BaseModel
from models.user import UserModel
from models.property_assignment import PropertyAssignment


class PropertyModel(BaseModel):
    __tablename__ = "properties"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    address = db.Column(db.String(250))
    unit = db.Column(db.String(20), default="")
    city = db.Column(db.String(50))
    state = db.Column(db.String(50))
    zipcode = db.Column(db.String(20))
    archived = db.Column(db.Boolean, default=False, nullable=False)

    leases = db.relationship(
        "LeaseModel", backref="property", lazy=True, cascade="all, delete-orphan"
    )
    managers = db.relationship(
        UserModel, secondary=PropertyAssignment.tablename(), backref="properties"
    )

    def json(self):

        managers_name = [manager.full_name() for manager in self.managers]

        return {
            "id": self.id,
            "name": self.name,
            "address": self.address,
            "unit": self.unit,
            "city": self.city,
            "state": self.state,
            "zipcode": self.zipcode,
            "propertyManager": [user.json() for user in self.managers]
            if self.managers
            else None,
            "lease": [lease.json() for lease in self.leases] if self.leases else None,
            "propertyManagerName": managers_name if managers_name else None,
            "archived": self.archived,
            "created_at": Time.format_date(self.created_at),
            "updated_at": Time.format_date(self.updated_at),
        }

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_manager(cls, manager_id):
        return cls.query.filter(cls.managers.any(UserModel.id == manager_id)).all()
