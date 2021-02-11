import pytest
from models.lease import LeaseModel


@pytest.fixture
def lease_attributes(faker):
    def _lease_attributes(unitNum, tenant, property, dateTimeStart, dateTimeEnd):
        return {
            "unitNum": unitNum,
            "tenantID": tenant.id,
            "propertyID": property.id,
            "dateTimeStart": dateTimeStart,
            "dateTimeEnd": dateTimeEnd,
            "occupants": faker.random_number(digits=2),
        }

    yield _lease_attributes


@pytest.fixture
def create_lease(faker, lease_attributes, create_property, create_tenant):
    def _create_lease(
        tenant=None,
        property=None,
        unitNum=None,
        dateTimeStart=None,
        dateTimeEnd=None,
    ):
        unitNum = unitNum or faker.building_number()
        tenant = tenant or create_tenant()
        property = property or create_property()
        dateTimeStart = dateTimeStart or faker.date_time_this_decade()
        dateTimeEnd = dateTimeEnd or faker.date_time_this_decade(
            before_now=False, after_now=True
        )
        lease = LeaseModel(
            **lease_attributes(unitNum, tenant, property, dateTimeStart, dateTimeEnd)
        )
        lease.save_to_db()
        return lease

    yield _create_lease
