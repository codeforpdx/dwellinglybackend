import re

from db import db
from nobiru.nobiru_list import NobiruList
from datetime import datetime, timedelta
from models.base_model import BaseModel
from utils.time import Time


class TicketModel(BaseModel):
    STATUSES = ("New", "In Progress", "Closed")

    NEW         = STATUSES[0]
    IN_PROGRESS = STATUSES[1]
    CLOSED      = STATUSES[2]

    for status in STATUSES:
        name = re.sub(r"\s", "_", status.lower())
        exec(f"""
@classmethod
def {name}(cls):
    return cls.query.filter_by(status='{status}')
        """)

    __tablename__ = "tickets"

    id = db.Column(db.Integer, primary_key=True)
    issue = db.Column(db.String(144))
    tenant_id = db.Column(db.Integer, db.ForeignKey("tenants.id"), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    status = db.Column(db.String, default=NEW, nullable=False)
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
            "author": self.author.full_name(),
            "status": self.status,
            "minsPastUpdate": minsPastUpdate,
            "urgency": self.urgency,
            "notes": self.notes.json(),
            "created_at": Time.format_date(self.created_at),
            "updated_at": Time.format_date(self.updated_at),
        }
