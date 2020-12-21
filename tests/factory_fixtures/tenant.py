import pytest
from models.tenant import TenantModel

@pytest.fixture
def create_tenant(faker, create_property):
    def _create_tenant(property=create_property()):
        tenant = TenantModel(
                firstName=faker.first_name(),
                lastName=faker.last_name(),
                phone=faker.phone_number(),
                propertyID=property.id,
                staffIDs=[]
            )
        tenant.save_to_db()
        return tenant
    yield _create_tenant
