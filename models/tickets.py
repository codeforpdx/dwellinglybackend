from sqlalchemy.orm import relationship
from db import db
from models.tenant import TenantModel
from models.user import UserModel
from models.notes import NotesModel
from models.tenant import TenantModel
from datetime import datetime

class TicketModel(db.Model):
    __tablename__ = "tickets"

    id = db.Column(db.Integer, primary_key=True)
    issue = db.Column(db.String(144))
    tenant = db.Column(db.Integer, db.ForeignKey('tenants.id'))
    assignedUser = db.Column(db.Integer, db.ForeignKey('users.id'))
    sender = db.Column(db.Integer, db.ForeignKey('users.id'))
    opened =  db.Column(db.DateTime, default=datetime.utcnow)
    updated = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(12))
    urgency = db.Column(db.String(12))
    notelog = db.Column(db.Text)

    #relationships
    notes = db.relationship(NotesModel)

    def __init__(self, issue, sender, tenant, status, urgency, assignedUser):
        self.issue = issue
        self.sender = sender
        self.tenant = tenant
        self.opened = datetime.now()
        self.updated = datetime.now()
        self.assignedUser = assignedUser
        self.status = status
        self.urgency = urgency


    def json(self):
        message_notes = []
        for note in self.notes:
            message_notes.append(note.json())

        senderData = UserModel.find_by_id(self.sender)
        senderName = "{} {}".format(senderData.firstName, senderData.lastName)

        tenantData = TenantModel.find_by_id(self.tenant)
        tenantName = "{} {}".format(tenantData.firstName, tenantData.lastName)

        assignedUserData = UserModel.find_by_id(self.assignedUser)
        assignedUser = "{} {}".format(assignedUserData.firstName, assignedUserData.lastName)

        # dateTimeStatusChange = datetime.strptime(self.updated, "%d-%b-%Y (%H:%M)")
        dateTimeNow = datetime.now()
        minsPastUpdate = int((dateTimeNow - self.updated).total_seconds() / 60)

        return {
            'id': self.id,
            'issue':self.issue,
            'tenant': tenantName,
            'senderID': self.sender,
            'tenantID': self.tenant,
            'assignedUserID': self.assignedUser,
            'sender': senderName,
            'assigned': assignedUser,
            'opened': self.opened.strftime("%m/%d/%Y, %H:%M:%S"),
            'updated':self.updated.strftime("%m/%d/%Y, %H:%M:%S"),
            'status': self.status,
            'minsPastUpdate': minsPastUpdate,
            'urgency': self.urgency,
            'notes': message_notes
        }


    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first() 

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
