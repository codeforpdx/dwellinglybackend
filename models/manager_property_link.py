from db import db
from models.base_model import BaseModel


class ManagerPropertyLink(BaseModel):
    __tablename__ = 'manager_property_links'

    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'), primary_key=True)
    manager_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
