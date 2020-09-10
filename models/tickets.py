from sqlalchemy.orm import relationship
from db import db
from models.tenant import TenantModel
from models.user import UserModel
from models.notes import NotesModel
from models.tenant import TenantModel
from datetime import datetime
from models.base_model import BaseModel


class TicketModel(BaseModel):
    __tablename__ = "tickets"

    id = db.Column(db.Integer, primary_key=True)
    issue = db.Column(db.String(144))
    tenant = db.Column(db.Integer, db.ForeignKey('tenants.id'))
    assignedUser = db.Column(db.Integer, db.ForeignKey('users.id'))
    sender = db.Column(db.Integer, db.ForeignKey('users.id'))
    opened =  db.Column(db.String(32))
    updated = db.Column(db.String(32))
    status = db.Column(db.String(12))
    urgency = db.Column(db.String(12))
    notelog = db.Column(db.Text)

    #relationships
    notes = db.relationship(NotesModel)

    def __init__(self, issue, sender, tenant, status, urgency, assignedUser):
        dateTime = datetime.now()
        timestamp = dateTime.strftime("%d-%b-%Y (%H:%M)")
        self.issue = issue
        self.sender = sender
        self.tenant = tenant
        self.opened = timestamp
        self.updated = timestamp
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

        dateTimeStatusChange = datetime.strptime(self.updated, "%d-%b-%Y (%H:%M)")
        dateTimeNow = datetime.now()
        minsPastUpdate = int((dateTimeNow - dateTimeStatusChange).total_seconds() / 60)

        return {
            'id': self.id,
            'issue':self.issue,
            'tenant': tenantName,
            'senderID': self.sender,
            'tenantID': self.tenant,
            'assignedUserID': self.assignedUser,
            'sender': senderName,
            'assigned': assignedUser,
            'opened': self.opened,
            'updated':self.updated,
            'status': self.status,
            'minsPastUpdate': minsPastUpdate,
            'urgency': self.urgency,
            'notes': message_notes
        }
        # notes.json() for note in self.notes.all()]
