import pytest
from models.tenant import TenantModel

@pytest.fixture
def create_tenant():
    def _create_tenant():
        tenant = TenantModel(
                firstName="firstName",
                lastName="lastName",
                phone="phone",
                propertyID=None,
                staffIDs=[],
                unitNum=3
            )
        tenant.save_to_db()
        return tenant
    yield _create_tenant
