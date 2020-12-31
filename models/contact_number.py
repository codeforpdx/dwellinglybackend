from db import db
from models.base_model import BaseModel
from utils.time import Time


class ContactNumberModel(BaseModel):
    __tablename__ = "contact_numbers"

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(20), nullable=False)
    numtype = db.Column(db.String(30))
    extension = db.Column(db.String(10))
    emergency_contact_id = db.Column(
        db.Integer, db.ForeignKey("emergency_contacts.id"), nullable=False
    )

    def json(self):
        return {
            "id": self.id,
            "number": self.number,
            "numtype": self.numtype,
            "extension": self.extension,
            "created_at": Time.format_date(self.created_at),
            "updated_at": Time.format_date(self.updated_at),
        }
