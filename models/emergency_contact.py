from sqlalchemy.orm import relationship
from db import db
from models.contact_number import ContactNumberModel


class EmergencyContactModel(db.Model):
    __tablename__ = "emergency_contacts"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(256))
    #relationships
    contact_numbers = relationship('ContactNumberModel', backref='contact_numbers', lazy=True)

    def __init__(self, name, contactNumbers, description=None):
        self.name = name
        self.description = description if description else ''
        self.contact_numbers = []
        for number in contactNumbers:
            #Need to revisit this... 
            #   contact numbers can be associated many-to-one  w.r.t. emergency contacts
            #   if a contact number exists already for one emergency contact, 
            #   and a second emergency contact claims that contact number as its own,
            #   Does the backref to the first emergency contact become invalid???
            item = ContactNumberModel.find_by_number(number['number'])
            if not item: 
                item = ContactNumberModel(
                    emergency_contact_id = self.id,
                    number = number['number'],
                    numtype = number['type'] if 'type' in number.keys() else '',
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
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
