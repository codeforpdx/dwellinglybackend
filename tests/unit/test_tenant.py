import pytest
from tests.unit.base_interface_test import BaseInterfaceTest
from models.tenant import TenantModel
from schemas.tenant import TenantSchema
from utils.time import Time


class TestBaseTenantModel(BaseInterfaceTest):
    def setup(self):
        self.object = TenantModel()
        self.custom_404_msg = "Tenant not found"
        self.schema = TenantSchema


@pytest.mark.usefixtures("empty_test_db")
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
            "staff": tenant.staff.json(),
            "lease": lease.json(),
            "created_at": Time.format_date(tenant.created_at),
            "updated_at": Time.format_date(tenant.updated_at),
            "archived": tenant.archived,
        }


@pytest.mark.usefixtures("empty_test_db")
class TestTenantFactory:
    def test_create_tenant(self, create_tenant):
        assert create_tenant()

    def test_create_tenant_with_staff_as_list(self, create_tenant, create_join_staff):
        staff = [create_join_staff().id for _ in range(3)]
        tenant = create_tenant(staff)
        assert [join_staff.id for join_staff in tenant.staff] == staff

    def test_create_tenant_with_staff_as_int(self, create_tenant, create_join_staff):
        number_of_staff = 4
        tenant = create_tenant(number_of_staff)
        assert len(tenant.staff) == number_of_staff
