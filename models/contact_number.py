from db import db


class ContactNumberModel(db.Model):
    __tablename__ = "contact_numbers"

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(20))
    numtype = db.Column(db.String(30))
    extension = db.Column(db.String(10))
    emergency_contact_id = db.Column(db.Integer, db.ForeignKey('emergency_contacts.id'), nullable=False)

    def __init__(self, emergency_contact_id, number, numtype='', extension=''):
        # self.id = id
        self.emergency_contact_id = emergency_contact_id
        self.number = number
        self.numtype = numtype if numtype else ''
        self.extension = extension if extension else ''

    def json(self):
        return {'id': self.id, 'number':self.number, 'numtype': self.numtype, 'extension': self.extension}

    @classmethod
    def find_by_number(cls, number):
        return cls.query.filter_by(number=number).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
