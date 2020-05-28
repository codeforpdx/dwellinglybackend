from db import db
from models.tickets import TicketModel
from models.user import UserModel
from datetime import datetime

class NotesModel(db.Model):
    __tablenname__ = "Notes"

    id = db.Column(db.Integer, primary_key=True)
    ticketid = db.Column(db.Integer, db.ForeignKey('tickets.id'))
    created = db.Column(db.String(32))
    # created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    text = db.Column(db.Text)

    def __init__(self, ticketid, text):
        dateTime = datetime.now()
        timestamp = dateTime.strftime("%d-%b-%Y (%H:%M:%S.%f)")
        self.ticketid = ticketid
        self.created = timestamp
        self.text = text

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def json(self):
        return {
            'id':self.id,
            'ticketid': self.ticketid,
            'created': self.created,
            'self.text': self.text
        }

    @classmethod
    def find_by_ticketid(cls, ticketid):
        return cls.query.filter_by(ticketid = ticketid).all()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id = id).first()
