from sqlalchemy import column, false, null

from nobiru.nobiru_query import NobiruQuery
from models.staff_tenant_link import StaffTenantLink


class TenantQuery(NobiruQuery):
    def active(self):
        return self.where(column("archived") == false())

    def unassigned_staff(self):
        return self.join(StaffTenantLink, isouter=True).where(
            StaffTenantLink.tenant_id == null()
        )
