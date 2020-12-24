import pytest
from models.tenant import TenantModel

@pytest.fixture
def create_tenant(faker):
    def _create_tenant():
        tenant = TenantModel(
                firstName=faker.first_name(),
                lastName=faker.last_name(),
                phone=faker.phone_number(),
                staffIDs=[]
            )
        tenant.save_to_db()
        return tenant
    yield _create_tenant
