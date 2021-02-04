from db import db
from models.tenant import TenantModel
from models.user import UserModel
from datetime import datetime, timedelta
from models.base_model import BaseModel
from utils.time import Time
import enum


class TicketStatus(str, enum.Enum):
    New = "New"
    In_Progress = "In Progress"
    Closed = "Closed"


class TicketModel(BaseModel):
    __tablename__ = "tickets"

    id = db.Column(db.Integer, primary_key=True)
    issue = db.Column(db.String(144))
    tenantID = db.Column(db.Integer, db.ForeignKey("tenants.id"))
    assignedUserID = db.Column(db.Integer, db.ForeignKey("users.id"))
    senderID = db.Column(db.Integer, db.ForeignKey("users.id"))
    status = db.Column(db.Enum(TicketStatus))
    urgency = db.Column(db.String(12))
    notelog = db.Column(db.Text)

    notes = db.relationship(
        "NotesModel", backref="ticket", lazy=False, cascade="all, delete-orphan"
    )

    def json(self):
        message_notes = []
        for note in self.notes:
            message_notes.append(note.json())

        senderData = UserModel.find_by_id(self.senderID)
        senderName = "{} {}".format(senderData.firstName, senderData.lastName)

        tenantData = TenantModel.find_by_id(self.tenantID)
        tenantName = "{} {}".format(tenantData.firstName, tenantData.lastName)

        assignedUserData = UserModel.find_by_id(self.assignedUserID)
        assignedUser = "{} {}".format(
            assignedUserData.firstName, assignedUserData.lastName
        )
        minsPastUpdate = int((datetime.utcnow() - self.updated_at).total_seconds() / 60)

        return {
            "id": self.id,
            "issue": self.issue,
            "tenant": tenantName,
            "senderID": self.senderID,
            "tenantID": self.tenantID,
            "assignedUserID": self.assignedUserID,
            "sender": senderName,
            "assigned": assignedUser,
            "status": self.status,
            "minsPastUpdate": minsPastUpdate,
            "urgency": self.urgency,
            "notes": message_notes,
            "created_at": Time.format_date(self.created_at),
            "updated_at": Time.format_date(self.updated_at),
        }

    # Get tickets with the given status
    @classmethod
    def find_count_by_status(cls, status):
        return cls.query.filter_by(status=status).count()

    # Get tickets updated with the given time and with the given status
    @classmethod
    def find_count_by_update_status(cls, status, minutes):
        # calculated in minutes: 1 day = 1440, 1 week = 10080
        dateTime = datetime.utcnow() - timedelta(minutes=minutes)
        return (
            db.session.query(TicketModel)
            .filter(TicketModel.updated_at >= dateTime)
            .filter(TicketModel.status == status)
            .count()
        )

    # Get tenant by ID
    @classmethod
    def find_by_tenantID(cls, tenantID):
        return cls.query.filter_by(tenantID=tenantID).all()
