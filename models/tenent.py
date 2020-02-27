from db import db

#basically a hash table to connect landlords, tenents, and properties
#hold off on implementation as it might redundent

class TenentModel(db.Model):
    __tablename__ = "tenents"

    id = db.Column(db.Integer, primary_key=True)
    tenentID = db.Column(db.Integer, db.ForeignKey('users.id'))
    propertyID = db.Column(db.Integer, db.ForeignKey('property.id'))
    landlordID = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, tenentID, propertyID, landlordID):
        self.id = id
        self.tenentID = tenentID
        self.propertyID = propertyID
        self.landlordID = landlordID

    def json(self):
        return {'id': self.id, 'name':self.name, 'address': self.address, 'city': self.city, 'state': self.state}
    
    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first() #SELECT * FROM property WHERE id = id LIMIT 1
    
    def find_by_tenent(cls, id):
        return cls.query.filter_by(tenentID = id).first()
    
    def find_by_property(cls, id):
        return cls.query.filter_by(propertyID = id).all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
