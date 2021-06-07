from db import db
from models.user import UserModel
from models.property_assignment import PropertyAssignment
from nobiru.nobiru_list import NobiruList


class PropertyManager(UserModel):
    __mapper_args__ = {"polymorphic_identity": "property_manager"}
