import pytest
from models.lease import LeaseModel


@pytest.fixture
def lease_attributes(faker):
    def _lease_attributes(unitNum, tenant, property):
        return {
            "unitNum": unitNum,
            "tenantID": tenant.id,
            "propertyID": property.id,
            "dateTimeStart": faker.date_time_this_decade(),
            "dateTimeEnd": faker.date_time_this_decade(
                before_now=False, after_now=True
            ),
            "occupants": faker.random_number(digits=2),
        }

    yield _lease_attributes


@pytest.fixture
def create_lease(
    faker, lease_attributes, create_property, create_tenant, tenant=None, property=None
):
    def _create_lease(tenant=tenant, property=property, unitNum=None):
        if not unitNum:
            unitNum = faker.building_number()
        tenant = tenant or create_tenant()
        property = property or create_property()
        lease = LeaseModel(**lease_attributes(unitNum, tenant, property))
        lease.save_to_db()
        return lease

    yield _create_lease
