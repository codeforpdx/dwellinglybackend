from db import db
from models.base_model import BaseModel


class ContactNumberModel(BaseModel):
    __tablename__ = "contact_numbers"

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(20))
    numtype = db.Column(db.String(30))
    extension = db.Column(db.String(10))
    emergency_contact_id = db.Column(db.Integer, db.ForeignKey('emergency_contacts.id'))

    def __init__(self, emergency_contact_id, number, numtype='', extension=''):
        self.emergency_contact_id = emergency_contact_id
        self.number = number
        self.numtype = numtype if numtype else ''
        self.extension = extension if extension else ''

    def json(self):
        return {'id': self.id, 'number':self.number, 'numtype': self.numtype, 'extension': self.extension}
