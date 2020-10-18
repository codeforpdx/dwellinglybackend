from db import db
from models.base_model import BaseModel
from utils.time import Time


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
        return {
            'id': self.id,
            'number':self.number,
            'numtype': self.numtype,
            'extension': self.extension,
            'created_at': Time.format_date(self.created_at) if self.created_at else None,
            'updated_at': Time.format_date(self.updated_at) if self.updated_at else None
        }
