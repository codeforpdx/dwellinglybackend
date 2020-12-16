from sqlalchemy.orm import relationship
from db import db
from models.user import UserModel
from models.base_model import BaseModel
from utils.time import Time


class TenantModel(BaseModel):
    __tablename__ = "tenants"

    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(100), nullable=False)
    lastName = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    propertyID = db.Column(db.Integer, db.ForeignKey('properties.id'))

    # relationships
    staff = relationship('UserModel', secondary='staff_tenant_links')
    leases = db.relationship('LeaseModel',
        backref='tenant', lazy=True, cascade="all, delete-orphan")

    def __init__(self, firstName, lastName, phone, propertyID, staffIDs):
        self.firstName = firstName
        self.lastName = lastName
        self.phone = phone
        self.propertyID = propertyID if propertyID else None
        self.staff = []
        if not (staffIDs == None):
            for id in staffIDs:
                user = UserModel.find_by_id(id)
                if user: self.staff.append(user)


    def json(self):
        return {
            'id': self.id,
            'firstName': self.firstName,
            'lastName': self.lastName,
            'fullName': '{} {}'.format(self.firstName, self.lastName),
            'phone': self.phone,
            'propertyID': self.propertyID,
            'propertyName': self.property.name if self.property else None,
            'staff': [user.json() for user in self.staff] if self.staff else [],
            'created_at': Time.format_date(self.created_at),
            'updated_at': Time.format_date(self.updated_at)
        }

    @classmethod
    def find_by_first_and_last(cls, first, last):
        return cls.query.filter_by(firstName=first, lastName=last).first()
