from db import db
from utils.time import Time
from marshmallow import ValidationError

from models.tenant import TenantModel
from models.base_model import BaseModel
from models.user import UserModel, RoleEnum
from models.property_assignment import PropertyAssignment


class PropertyModel(BaseModel):
    __tablename__ = "properties"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    address = db.Column(db.String(250))
    unit = db.Column(db.String(20), default="")
    city = db.Column(db.String(50))
    state = db.Column(db.String(50))
    zipcode = db.Column(db.String(20))
    archived = db.Column(db.Boolean)

    tenants = db.relationship(TenantModel, backref="property")
    leases = db.relationship('LeaseModel',
        backref='property', lazy=True, cascade="all, delete-orphan")
    managers = db.relationship(UserModel, secondary='property_assignments', backref='properties')

    def __init__(self, name, address, unit, city, state, zipcode, propertyManagerIDs, archived):
        self.name = name
        self.address = address
        self.unit = unit
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.managers = self.set_property_managers(propertyManagerIDs)
        self.archived = False

    def json(self):
        property_tenants = []
        for tenant in self.tenants:
            property_tenants.append(tenant.id)

        managers_name = [manager.fullName for manager in self.managers]

        return {
            'id': self.id,
            'name':self.name,
            'address': self.address,
            'unit': self.unit,
            'city': self.city,
            'state': self.state,
            'zipcode': self.zipcode,
            'propertyManager': [user.json() for user in self.managers] if self.managers else None,
            'propertyManagerName': managers_name if managers_name else None,
            'tenantIDs': property_tenants,
            'archived': self.archived,
            'created_at': Time.format_date(self.created_at),
            'updated_at': Time.format_date(self.updated_at)
        }

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_manager(cls, manager_id):
        return cls.query.filter(cls.managers.any(UserModel.id == manager_id)).all()

    @classmethod
    def set_property_managers(cls, ids):
        managers = []
        if ids:
            for id in ids:
                user = UserModel.find_by_id(id)
                if user and user.role == RoleEnum.PROPERTY_MANAGER:
                    managers.append(user)
                elif user and user.role != RoleEnum.PROPERTY_MANAGER:
                    raise ValidationError(f'{user.fullName} is not a property manager')
                else:
                    raise ValidationError(f'{id} is not a valid user id')
        return managers
