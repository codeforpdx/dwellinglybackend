import datetime
from db import db

class LeaseModel(db.Model):
    __tablename__ = "lease"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    unit = db.Column(db.String(20))
    landlordID = db.Column(db.Integer)
    propertyID = db.Column(db.Integer)
    dateStart = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    dateEnd = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    dateUpdated = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, id, name, unit, landlordID, propertyID, dateStart, dateEnd, dateUpdated):
        self.id = id
        self.name = name
        self.unit = unit
        self.landlordID = landlordID
        self.propertyID = propertyID
        self.dateStart = dateStart
        self.dateEnd = dateEnd
        self.dateUpdate = dateUpdated

    def json(self):
        return {'id': self.id, 'name':self.name, 'propertyID':self.propertyID, 'landlordID': self.landlordID, 'unit': unit, 'dateStart': self.dateStart, 'dateEnd': self.dateEnd, 'dateUpdate': self.dateUpdated}
    
    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first() #SELECT * FROM property WHERE id = id LIMIT 1

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

