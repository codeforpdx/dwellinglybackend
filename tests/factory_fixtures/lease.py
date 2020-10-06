import pytest
from models.lease import LeaseModel
from datetime import datetime

@pytest.fixture
def lease_attributes():
    def _lease_attributes(name, tenant, property):
        return {
            "name": name,
            "tenantID": tenant.id,
            "propertyID": property.id,
            "dateTimeStart": datetime.now(),
            "dateTimeEnd": datetime.now(),
            "dateUpdated": datetime.now(),
            "occupants": 3
        }
    yield _lease_attributes

@pytest.fixture
def create_lease(lease_attributes, create_property, create_tenant):
    def _create_lease(name="Hello World", tenant=create_tenant(), property=create_property()):
        lease = LeaseModel(**lease_attributes(name, tenant, property))
        lease.save_to_db()
        return lease
    yield _create_lease
