from db import db
from models.user import UserModel
from models.staff_tenant_link import StaffTenantLink
from nobiru.nobiru_list import NobiruList


class Admin(UserModel):
    __mapper_args__ = {"polymorphic_identity": "admin"}

    tenants = db.relationship(
        "TenantModel",
        secondary=StaffTenantLink.tablename(),
        collection_class=NobiruList,
        viewonly=True,
    )

    def is_admin(self):
        return True

    def has_staff_privs(self):
        return True

    def has_pm_privs(self):
        return True

    def serialize(self):
        return {"tenants": self.tenants.json(include_staff=False)}
