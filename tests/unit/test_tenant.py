from tests.unit.base_interface_test import BaseInterfaceTest
from models.tenant import TenantModel
from schemas.tenant import TenantSchema
from utils.time import Time


class TestBaseTenantModel(BaseInterfaceTest):
    def setup(self):
        self.object = TenantModel()
        self.custom_404_msg = "Tenant not found"
        self.schema = TenantSchema


class TestTenantModel:
    def test_json(self, create_tenant, create_lease):
        tenant = create_tenant()
        lease = create_lease(tenant=tenant)

        assert tenant.json() == {
            "id": tenant.id,
            "firstName": tenant.firstName,
            "lastName": tenant.lastName,
            "fullName": "{} {}".format(tenant.firstName, tenant.lastName),
            "phone": tenant.phone,
            "staff": tenant.staff,
            "lease": lease.json(),
            "created_at": Time.format_date(tenant.created_at),
            "updated_at": Time.format_date(tenant.updated_at),
            "archived": tenant.archived,
        }


class TestTenantFactory:
    def test_create_tenant(self, create_tenant):
        assert create_tenant()
