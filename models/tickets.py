from sqlalchemy.orm import relationship
from db import db
from models.tenant import TenantModel
from models.user import UserModel
from datetime import datetime

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


class TicketModel(db.Model):
    __tablename__ = "tickets"

    id = db.Column(db.Integer, primary_key=True)
    issue = db.Column(db.String(144))
    tenant = db.Column(db.Integer, db.ForeignKey('tenants.id'))
    sender = db.Column(db.Integer, db.ForeignKey('users.id'))
    opened =  db.Column(db.String(32))
    status = db.Column(db.String(12))
    urgency = db.Column(db.String(12))

    #relationships
    notes = db.relationship('NotesModel', lazy='dynamic')

    def __init__(self, issue, sender, tenant, status, urgency):
        dateTime = datetime.now()
        timestamp = dateTime.strftime("%d-%b-%Y (%H:%M:%S.%f)")
        self.issue = issue
        self.tenant = tenant
        self.sender = sender
        self.opened = timestamp
        self.status = status
        self.urgency = urgency

    def json(self):
        return {
            'id': self.id,
            'issue':self.issue,
            'tenant': self.tenant,
            'sender': self.sender,
            'opened': self.opened,
            'status': self.status,
            'notes': [notes.json() for note in self.notes.all()]
        }

    # @classmethod
    #  def find_all(cls):
    #     return cls.query.all()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first() #SELECT * FROM property WHERE id = id LIMIT 1

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
