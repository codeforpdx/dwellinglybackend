from db import db
from datetime import datetime

class NotesModel(db.Model):
    __tablenname__ = "Notes"

    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.String(32))
    text = db.Column(db.Text)

    ticket = db.relationship('TicketModel')
    ticketid = db.Column(db.Integer, db.ForeignKey('tickets.id'))

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
            'text': self.text
        }

    @classmethod
    def find_by_ticketid(cls, ticketid):
        return cls.query.filter_by(ticketid = ticketid).all()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id = id).first()
