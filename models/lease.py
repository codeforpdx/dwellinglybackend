import datetime
from db import db

class LeaseModel(db.Model):
    __tablename__ = "lease"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    landlordID = db.Column(db.Integer(), db.ForeignKey('users.id'))
    propertyID = db.Column(db.Integer, db.ForeignKey('properties.id'))
    tenantID = db.Column(db.Integer)
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

        return {
          'id': self.id,
          'name':self.name,
          'propertyID':self.propertyID,
          'landlordID': self.landlordID,
          'tenantID': self.tenantID,
          'dateTimeStart': self.dateTimeStart.strftime("%m/%d/%Y %H:%M:%S"),
          'dateTimeEnd': self.dateTimeEnd.strftime("%m/%d/%Y %H:%M:%S"),
          'occupants': self.occupants
        }

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first() #SELECT * FROM property WHERE id = id LIMIT 1

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
