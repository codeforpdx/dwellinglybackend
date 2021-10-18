from db import db
from nobiru.nobiru_list import NobiruList
from models.base_model import BaseModel
from models.user import UserModel
from models.property_assignment import PropertyAssignment
from utils.time import Time


class PropertyModel(BaseModel):
    __tablename__ = "properties"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    address = db.Column(db.String(250), nullable=False)
    num_units = db.Column(db.Integer, default=1)
    city = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    zipcode = db.Column(db.String(20), nullable=False)
    archived = db.Column(db.Boolean, default=False, nullable=False)

    leases = db.relationship(
        "LeaseModel",
        backref="property",
        lazy=True,
        cascade="all, delete-orphan",
        collection_class=NobiruList,
    )

    managers = db.relationship(
        "PropertyManager",
        secondary=PropertyAssignment.tablename(),
        back_populates="properties",
        collection_class=NobiruList,
    )

    def validation_context(self):
        return {"name": self.name}

    def json(self, include_tenants=False, include_managers=True):
        property = {
            "id": self.id,
            "name": self.name,
            "address": self.address,
            "num_units": self.num_units,
            "city": self.city,
            "state": self.state,
            "zipcode": self.zipcode,
            "leases": self.leases.json(),
            "archived": self.archived,
            "created_at": Time.format_date(self.created_at),
            "updated_at": Time.format_date(self.updated_at),
        }
        if include_tenants:
            property["tenants"] = self.tenants()

        if include_managers:
            property["propertyManagers"] = self.managers.json()

        return property

    def tenants(self):
        tenants = []
        for lease in self.leases:
            if lease.is_active():
                tenants.append(lease.tenant.json())
        return tenants

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_manager(cls, manager_id):
        return cls.query.filter(cls.managers.any(UserModel.id == manager_id)).all()
