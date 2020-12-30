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
class TestTenantFactory:
    def test_create_tenant(self, create_tenant):
        assert create_tenant()
