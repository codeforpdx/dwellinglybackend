from sqlalchemy.orm import relationship
from db import db
from models.contact_number import ContactNumberModel
from models.base_model import BaseModel


class EmergencyContactModel(BaseModel):
    __tablename__ = "emergency_contacts"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(256))
    #relationships
    contact_numbers = relationship('ContactNumberModel', backref='contact_numbers', lazy=True)

    def __init__(self, name, contact_numbers, description=None):
        self.name = name
        self.description = description if description else ''
        self.contact_numbers = []
        for number in contact_numbers:
            item = ContactNumberModel(
                emergency_contact_id = self.id,
                number = number['number'],
                numtype = number['numtype'] if 'numtype' in number.keys() else '',
                extension = number['extension'] if 'extension' in number.keys() else '',
            )
            db.session.add(item)
            self.contact_numbers.append(item)

    def json(self):
        return {
            'id': self.id,
            'name':self.name,
            'description': self.description,
            'contact_numbers': [number.json() for number in self.contact_numbers]
        }

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()
