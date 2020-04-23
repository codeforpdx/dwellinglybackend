from db import db

#basically a hash table to connect landlords, tenants, and properties
#hold off on implementation as it might redundent

class TenantModel(db.Model):
    __tablename__ = "tenants"

    id = db.Column(db.Integer, primary_key=True)
    tenantID = db.Column(db.Integer, db.ForeignKey('users.id'))
    propertyID = db.Column(db.Integer, db.ForeignKey('property.id'))
    landlordID = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, tenantID, propertyID, landlordID):
        self.id = id
        self.tenantID = tenantID
        self.propertyID = propertyID
        self.landlordID = landlordID

    def json(self):
        return {'id': self.id, 'name':self.name, 'address': self.address, 'city': self.city, 'state': self.state}
    
    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first() #SELECT * FROM property WHERE id = id LIMIT 1
    
    def find_by_tenant(cls, id):
        return cls.query.filter_by(tenantID = id).first()
    
    def find_by_property(cls, id):
        return cls.query.filter_by(propertyID = id).all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
