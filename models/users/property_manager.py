from db import db
from models.user import UserModel
from models.property_assignment import PropertyAssignment
from nobiru.nobiru_list import NobiruList


class PropertyManager(UserModel):
    __mapper_args__ = {"polymorphic_identity": "property_manager"}

    properties = db.relationship(
        "PropertyModel",
        secondary=PropertyAssignment.tablename(),
        collection_class=NobiruList,
        viewonly=True,
    )

    def has_pm_privs(self):
        return True

    def serialize(self):
        return {"properties": self.properties.json(include_managers=False)}
