import pytest
from faker import Faker
from models.tenant import TenantModel

@pytest.fixture
def create_tenant(create_property):
    def _create_tenant(property=create_property()):
        fake = Faker()
        tenant = TenantModel(
                firstName=fake.unique.first_name(),
                lastName=fake.unique.last_name(),
                phone=fake.phone_number(),
                propertyID=property.id,
                staffIDs=[]
            )
        tenant.save_to_db()
        return tenant
    yield _create_tenant
