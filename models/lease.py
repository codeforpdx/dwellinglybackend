import datetime
from db import db
from models.property import PropertyModel
from models.user import UserModel
from models.tenant import TenantModel
from models.base_model import BaseModel


class LeaseModel(BaseModel):
    __tablename__ = "lease"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    landlordID = db.Column(db.Integer(), db.ForeignKey('users.id'))
    propertyID = db.Column(db.Integer, db.ForeignKey('properties.id'))
    tenantID = db.Column(db.Integer, db.ForeignKey('tenants.id'))
    occupants = db.Column(db.Integer)
    dateTimeStart = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    dateTimeEnd = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    dateUpdated = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, name, tenantID, landlordID, propertyID, dateTimeStart, dateTimeEnd, dateUpdated, occupants):
        self.name = name
        self.landlordID = landlordID
        self.propertyID = propertyID
        self.tenantID = tenantID
        self.dateTimeStart = dateTimeStart
        self.dateTimeEnd = dateTimeEnd
        self.dateUpdated = dateUpdated
        self.occupants = occupants

    def json(self):
        property = PropertyModel.find_by_id(self.propertyID)
        landlord = UserModel.find_by_id(self.landlordID)
        tenant = TenantModel.find_by_id(self.tenantID)

        return {
          'id': self.id,
          'name':self.name,
          'propertyID': property.json(),
          'landlordID': landlord.json(),
          'tenantID': tenant.json(),
          'dateTimeStart': self.dateTimeStart.strftime("%m/%d/%Y %H:%M:%S"),
          'dateTimeEnd': self.dateTimeEnd.strftime("%m/%d/%Y %H:%M:%S"),
          'dateUpdated': self.dateUpdated.strftime("%m/%d/%Y %H:%M:%S"),
          'occupants': self.occupants
        }
