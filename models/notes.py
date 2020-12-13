from db import db
import models.user
from models.base_model import BaseModel
from utils.time import Time


class NotesModel(BaseModel):
    __tablename__ = "Notes"

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)
    userid = db.Column(db.Integer, db.ForeignKey('users.id'),
        nullable=False)

    ticketid = db.Column(db.Integer, db.ForeignKey('tickets.id'),
        nullable=False)

    def json(self):
        userobj = models.user.UserModel.find_by_id(self.userid)

        return {
            'id':self.id,
            'ticketid': self.ticketid,
            'text': self.text,
            'user': userobj.full_name(),
            'created_at': Time.format_date(self.created_at),
            'updated_at': Time.format_date(self.updated_at)
        }
