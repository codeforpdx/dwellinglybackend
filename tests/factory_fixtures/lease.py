import pytest
from models.lease import LeaseModel
from datetime import datetime

@pytest.fixture
def lease_attributes():
    def _lease_attributes(unitNum, tenant, property):
        return {
            "unitNum": unitNum,
            "tenantID": tenant.id,
            "propertyID": property.id,
            "dateTimeStart": datetime.utcnow(),
            "dateTimeEnd": datetime.utcnow(),
            "occupants": 3
        }
    yield _lease_attributes

@pytest.fixture
def create_lease(lease_attributes, create_property, create_tenant):
    def _create_lease(unitNum="D404"):
        tenant = create_tenant()
        lease = LeaseModel(**lease_attributes(unitNum, tenant, tenant.property))
        lease.save_to_db()
        return lease
    yield _create_lease
