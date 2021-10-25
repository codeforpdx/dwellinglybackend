from db import db
from models.base_model import BaseModel
from utils.time import Time
from datetime import datetime


class LeaseModel(BaseModel):
    __tablename__ = "lease"

    id = db.Column(db.Integer, primary_key=True)
    propertyID = db.Column(db.Integer, db.ForeignKey("properties.id"), nullable=False)
    tenantID = db.Column(
        db.Integer, db.ForeignKey("tenants.id"), unique=True, nullable=False
    )
    occupants = db.Column(db.Integer)
    dateTimeStart = db.Column(db.DateTime, nullable=False)
    dateTimeEnd = db.Column(db.DateTime, nullable=False)
    unitNum = db.Column(db.String(10))

    def json(self):
        return {
            "id": self.id,
            "propertyID": self.propertyID,
            "tenantID": self.tenantID,
            "occupants": self.occupants,
            "dateTimeStart": Time.format_date(self.dateTimeStart),
            "dateTimeEnd": Time.format_date(self.dateTimeEnd),
            "unitNum": self.unitNum,
        }

    def is_active(self):
        now = datetime.now()
        return now > self.dateTimeStart and now < self.dateTimeEnd
