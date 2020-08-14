from db import db
from datetime import datetime
from models.user import UserModel

class NotesModel(db.Model):
    __tablename__ = "Notes"

    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.String(32))
    text = db.Column(db.Text)
    user = db.Column(db.Integer, db.ForeignKey('users.id'))

    ticket = db.relationship('TicketModel')
    ticketid = db.Column(db.Integer, db.ForeignKey('tickets.id'))

    def __init__(self, ticketid, text, user):
        dateTime = datetime.now()
        timestamp = dateTime.strftime("%d-%b-%Y (%H:%M:%S.%f)")
        self.ticketid = ticketid
        self.created = timestamp
        self.text = text
        self.user = user

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def json(self):
        user = UserModel.find_by_id(self.user)

        return {
            'id':self.id,
            'ticketid': self.ticketid,
            'created': self.created,
            'text': self.text,
            'user': user.fullName
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id = id).first()
