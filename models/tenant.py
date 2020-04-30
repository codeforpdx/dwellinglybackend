from sqlalchemy.orm import relationship
from db import db
from models.user import UserModel

class TenantModel(db.Model):
    __tablename__ = "tenants"

    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(100))
    lastName = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    propertyID = db.Column(db.Integer, db.ForeignKey('property.id'))
    staffIDs = departments = relationship(
        UserModel,
        secondary='tenant_staff_link'
    )
    # leaseID = db.Column(db.Integer, db.ForeignKey('lease.id'))


    def __init__(self, firstName, lastName, phone, propertyID):
        self.id = id
        self.firstName = firstName
        self.lastName = lastName
        self.phone = phone
        self.propertyID = propertyID

    def json(self):
        return {
            'id': self.id, 
            'firstName':self.firstName, 
            'lastName':self.lastName, 
            'phone': self.phone, 
            'propertyID': self.propertyID,
            'staffIDs': self.staffIDs
        }
    
    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first() #SELECT * FROM property WHERE id = id LIMIT 1

    @classmethod
    def find_by_property(cls, id):
        return cls.query.filter_by(propertyID = id).all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
