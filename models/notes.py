from db import db
from models.base_model import BaseModel
from utils.time import Time


class NotesModel(BaseModel):
    __tablename__ = "Notes"

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    ticket_id = db.Column(db.Integer, db.ForeignKey("tickets.id"), nullable=False)

    def json(self):

        return {
            "id": self.id,
            "ticket_id": self.ticket_id,
            "text": self.text,
            "user": self.user.full_name(),
            "created_at": Time.format_date(self.created_at),
            "updated_at": Time.format_date(self.updated_at),
        }
