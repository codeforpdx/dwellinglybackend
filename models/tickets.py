from db import db
from nobiru.nobiru_list import NobiruList
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
    tenant_id = db.Column(db.Integer, db.ForeignKey("tenants.id"), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    status = db.Column(db.Enum(TicketStatus), default=TicketStatus.New, nullable=False)
    urgency = db.Column(db.String(12))

    notes = db.relationship(
        "NotesModel",
        backref="ticket",
        lazy=False,
        cascade="all, delete-orphan",
        collection_class=NobiruList,
    )

    def json(self):
        minsPastUpdate = int((datetime.utcnow() - self.updated_at).total_seconds() / 60)

        return {
            "id": self.id,
            "issue": self.issue,
            "tenant": "{} {}".format(self.tenant.firstName, self.tenant.lastName),
            "author_id": self.author_id,
            "tenant_id": self.tenant_id,
            "assigned_staff": self.tenant.staff.json(),
            "sender": self.author.full_name(),
            "status": self.status,
            "minsPastUpdate": minsPastUpdate,
            "urgency": self.urgency,
            "notes": self.notes.json(),
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
