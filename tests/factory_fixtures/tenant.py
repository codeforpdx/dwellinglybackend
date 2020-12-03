import pytest
from models.tenant import TenantModel

@pytest.fixture
def create_tenant(create_property):
    def _create_tenant(property=create_property()):
        tenant = TenantModel(
                firstName="firstName",
                lastName="lastName",
                phone="phone",
                propertyID=property.id,
                staffIDs=[]
            )
        tenant.save_to_db()
        return tenant
    yield _create_tenant
