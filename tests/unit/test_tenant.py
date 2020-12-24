import pytest
from tests.unit.base_interface_test import BaseInterfaceTest
from models.tenant import TenantModel
from schemas.tenant import TenantSchema



class TestBaseTenantModel(BaseInterfaceTest):
    def setup(self):
        self.object = TenantModel()
        self.custom_404_msg = 'Tenant not found'
        self.schema = TenantSchema


@pytest.mark.usefixtures('empty_test_db')
class TestTenant:
    def test_tenant_creation(self, tenant_attributes, create_property, create_join_staff):
        staff_1 = create_join_staff()
        staff_2 = create_join_staff()

        tenant_attrs = tenant_attributes(staff=[staff_1.id, staff_2.id])

        tenant = TenantModel.create(schema=TenantSchema, payload=tenant_attrs)

        assert tenant
        assert tenant.staff == [staff_1, staff_2]


@pytest.mark.usefixtures('empty_test_db')
class TestTenantFactory:
    def test_create_tenant(self, create_tenant):
        assert create_tenant()
