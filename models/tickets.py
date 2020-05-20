from sqlalchemy.orm import relationship
from db import db
from models.tenant import TenantModel
from mdoels.user import UserModel

#  id: 'K-0089ttxqQX-2',
#     issue: 'Property Damage',
#     tenant: {
#       address: 'Magnolia Park, Unit #2',
#       name: 'Alex Alder',
#       number: '503-555-1234'
#     },
#     sender: {
#       name: 'Tom Smith',
#       number: '541-123-4567'
#     },
#     sent: new Date('2017/12/19').toString(),
#     status: 'New',
#     urgency: 'Low',
#     notes: []


class PropertyModel(db.Model):
    __tablename__ = "Tickets"

    id = db.Column(db.Integer, primary_key=True)
    issue = db.Column(db.String(144))
    tenant = db.Column(db.Integer, db.ForeignKey('tenants.id'))
    sender = db.Column(db.Integer, db.ForeignKey('user.id'))
    opened =  db.Column(db.String(144))
    status = db.Column(db.String(12))
    urgency = db.Column(db.String(12))

    #relationships
    tenant = relationship('TenantModel')

    def __init__(self, issue, tenant, sender, opened, status, urgency):
        self.issue = issue
        self.tenant = tenant
        self.sender = sender
        self.opened = opened
        self.status = status
        self.urgency = urgency
        self.notes = []

    def json(self):
        return {
            'id': self.id, 
            'issue':self.issue, 
            'tenant': self.tenant, 
            'sender': self.sender, 
            'opened': self.opened, 
            'status': self.status,
            'notes': self.notes
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
