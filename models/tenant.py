from sqlalchemy.orm import relationship
from db import db
from models.user import UserModel
from models.base_model import BaseModel


class TenantModel(BaseModel):
    __tablename__ = "tenants"

    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(100))
    lastName = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    propertyID = db.Column(db.Integer, db.ForeignKey('properties.id'))
    # leaseID = db.Column(db.Integer, db.ForeignKey('lease.id'))
    addedOn = db.Column(db.Date())
    unit = db.Column(db.String(20))

    # relationships
    staff = relationship('UserModel', secondary='staff_tenant_links')

    def __init__(self, firstName, lastName, phone, propertyID, staffIDs, unit, addedOn):
        self.firstName = firstName
        self.lastName = lastName
        self.phone = phone
        self.propertyID = propertyID if propertyID else None
        self.staff = []
        for id in staffIDs:
            user = UserModel.find_by_id(id)
            if user: self.staff.append(user)
        self.unit = unit
        self.addedOn = addedOn


    def json(self):
        return {
            'id': self.id,
            'firstName':self.firstName,
            'lastName':self.lastName,
            'phone': self.phone,
            'propertyID': self.propertyID,
            'propertyName': self.property.name if self.property else None,
            'staff': [user.json() for user in self.staff] if self.staff else None,
            'unit': self.unit,
            'addedOn': self.addedOn
        }

    @classmethod
    def find_by_first_and_last(cls, first, last):
        return cls.query.filter_by(firstName = first, lastName = last).first()
