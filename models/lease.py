import datetime
from db import db

class LeaseModel(db.Model):
    __tablename__ = "lease"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    unit = db.Column(db.String(20))
    landlordID = db.Column(db.Integer), db.ForeignKey('users.id')
    propertyID = db.Column(db.Integer, db.ForeignKey('properties.id'))
    userID = db.Column(db.Integer, db.ForeignKey('users.id'))
    dateStart = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    dateEnd = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    dateUpdated = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    timeStart = db.Column(db.String(20))
    timeEnd = db.Column(db.String(20))
    occupants = db.Column(db.Integer)

    def __init__(self, id, name, unit, landlordID, propertyID, dateStart, dateEnd, dateUpdated, timeStart, timeEnd, occupants):
        self.id = id
        self.name = name
        self.unit = unit
        self.landlordID = landlordID
        self.propertyID = propertyID
        self.dateStart = dateStart
        self.dateEnd = dateEnd
        self.dateUpdate = dateUpdated
        self.timeStart = timeStart
        self.timeEnd = timeEnd
        self.occupants = occupants

    def json(self):
        return {
          'id': self.id,
          'name':self.name,
          'propertyID':self.propertyID,
          'landlordID': self.landlordID,
          'unit': self.unit,
          'dateStart': self.dateStart,
          'dateEnd': self.dateEnd,
          'dateUpdate': self.dateUpdated,
          'timeStart': self.timeStart,
          'timeEnd': self.timeEnd,
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
