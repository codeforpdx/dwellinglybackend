from db import db
from models.user import UserModel
from models.base_model import BaseModel
from utils.time import Time


class NotesModel(BaseModel):
    __tablename__ = "Notes"

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)
    user = db.Column(db.Integer, db.ForeignKey('users.id'))

    ticketid = db.Column(db.Integer, db.ForeignKey('tickets.id'),
        nullable=False)

    def json(self):
        user = UserModel.find_by_id(self.user)

        return {
            'id':self.id,
            'ticketid': self.ticketid,
            'text': self.text,
            'user': user.full_name(),
            'created_at': Time.format_date(self.created_at),
            'updated_at': Time.format_date(self.updated_at)
        }
