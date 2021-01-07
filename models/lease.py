from db import db
from models.base_model import BaseModel


class LeaseModel(BaseModel):
    __tablename__ = "lease"

    id = db.Column(db.Integer, primary_key=True)
    propertyID = db.Column(db.Integer, db.ForeignKey("properties.id"), nullable=False)
    tenantID = db.Column(db.Integer, db.ForeignKey("tenants.id"), nullable=False)
    occupants = db.Column(db.Integer)
    dateTimeStart = db.Column(db.DateTime, nullable=False)
    dateTimeEnd = db.Column(db.DateTime, nullable=False)
    unitNum = db.Column(db.String(10))
