import pytest
from tests.unit.base_interface_test import BaseInterfaceTest
from models.property import PropertyModel
from models.tenant import TenantModel
from schemas.tenant import TenantSchema
from utils.time import Time
import datetime


class TestBaseTenantModel(BaseInterfaceTest):
    def setup(self):
        self.object = TenantModel()
        self.custom_404_msg = "Tenant not found"
        self.schema = TenantSchema


@pytest.mark.usefixtures("empty_test_db")
class TestTenantModel:
    def test_only_active_lease_returned(self, faker, create_lease, create_tenant):
        tenant = create_tenant()

        # Create an expired lease for the tenant
        lease_expired_end = faker.date_time_this_decade(
            before_now=True, after_now=False
        )
        lease_expired_start = lease_expired_end - datetime.timedelta(days=365)
        lease_expired = create_lease(
            tenant=tenant,
            dateTimeStart=lease_expired_start,
            dateTimeEnd=lease_expired_end,
        )

        # Create an active lease for the tenant
        lease_active = create_lease(
            tenant=tenant, property=PropertyModel.find(lease_expired.propertyID)
        )

        # Active lease should be the only one that shows up
        assert tenant.json()["lease"] == lease_active.json()

    @pytest.mark.usefixtures("empty_test_db")
    class TestTenantFactory:
        def test_create_tenant(self, create_tenant):
            assert create_tenant()

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
