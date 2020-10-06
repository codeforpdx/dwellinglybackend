from sqlalchemy.orm import relationship
from db import db
from models.tenant import TenantModel
from models.base_model import BaseModel
from models.user import UserModel


class PropertyModel(BaseModel):
    __tablename__ = "properties"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    address = db.Column(db.String(250))
    unit = db.Column(db.String(20), default="")
    city = db.Column(db.String(50))
    state = db.Column(db.String(50))
    zipcode = db.Column(db.String(20))
    propertyManager = db.Column(db.Integer(), db.ForeignKey('users.id'))
    dateAdded = db.Column(db.String(50))
    archived = db.Column(db.Boolean)

    tenants = db.relationship(TenantModel, backref="property")

    def __init__(self, name, address, unit, city, state, zipcode, propertyManager, dateAdded, archived):
        self.name = name
        self.address = address
        self.unit = unit
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.propertyManager = propertyManager
        self.dateAdded = dateAdded
        self.archived = False

    def json(self):
        property_tenants = []
        for tenant in self.tenants:
            property_tenants.append(tenant.id)

        property_manager = UserModel.find_by_id(self.propertyManager)

        return {
            'id': self.id,
            'name':self.name,
            'address': self.address,
            'unit': self.unit,
            'city': self.city,
            'state': self.state,
            'zipcode': self.zipcode,
            'propertyManager': self.propertyManager,
            'propertyManagerName': property_manager.full_name() if property_manager else None,
            'tenantIDs': property_tenants,
            'dateAdded': self.dateAdded,
            'archived': self.archived
        }

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_manager(cls, manager_id):
        return cls.query.filter_by(propertyManager=manager_id).all()
