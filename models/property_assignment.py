from db import db
from models.base_model import BaseModel


class PropertyAssignment(BaseModel):
    __tablename__ = 'property_assignments'

    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'), primary_key=True)
    manager_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
