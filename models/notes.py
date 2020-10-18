from db import db
from models.user import UserModel
from models.base_model import BaseModel


class NotesModel(BaseModel):
    __tablename__ = "Notes"

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)
    user = db.Column(db.Integer, db.ForeignKey('users.id'))

    ticket = db.relationship('TicketModel')
    ticketid = db.Column(db.Integer, db.ForeignKey('tickets.id'))

    def __init__(self, ticketid, text, user):
        self.ticketid = ticketid
        self.text = text
        self.user = user

    def json(self):
        user = UserModel.find_by_id(self.user)

        return {
            'id':self.id,
            'ticketid': self.ticketid,
            'text': self.text,
            'user': user.fullName,
            'created_at': self.created_at.strftime("%m/%d/%Y %H:%M:%S") if self.created_at else None,
            'updated_at': self.updated_at.strftime("%m/%d/%Y %H:%M:%S") if self.updated_at else None
        }
