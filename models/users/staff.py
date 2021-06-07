from db import db
from models.user import UserModel
from models.staff_tenant_link import StaffTenantLink
from nobiru.nobiru_list import NobiruList


class Staff(UserModel):
    __mapper_args__ = {"polymorphic_identity": "staff"}
