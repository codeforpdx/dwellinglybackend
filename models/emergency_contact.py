from sqlalchemy.orm import relationship
from db import db
from models.base_model import BaseModel
from utils.time import Time


class EmergencyContactModel(BaseModel):
    __tablename__ = "emergency_contacts"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True, index=True)
    description = db.Column(db.String(256))

    contact_numbers = relationship(
        'ContactNumberModel',
        backref='contact_numbers',
        lazy=True,
        cascade="all, delete-orphan"
    )

    def json(self):
        return {
            'name':self.name,
            'description': self.description,
            'contact_numbers': [number.json() for number in self.contact_numbers],
            'created_at': Time.format_date(self.created_at),
            'updated_at': Time.format_date(self.updated_at)
        }

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()
