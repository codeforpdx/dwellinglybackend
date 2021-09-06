import pytest
from models.lease import LeaseModel
from schemas.lease import LeaseSchema
from utils.time import Time


def lease_attrs(faker, unitNum=None, dateTimeStart=None, dateTimeEnd=None):
    return {
        "unitNum": unitNum or faker.building_number(),
        "dateTimeStart": Time.to_iso(dateTimeStart or faker.date_time_this_decade()),
        "dateTimeEnd": Time.to_iso(
            dateTimeEnd or faker.date_time_this_decade(before_now=False, after_now=True)
        ),
        "occupants": faker.random_number(digits=2),
    }


@pytest.fixture
def lease_payload(faker, create_property):
    def _lease_payload():
        return {
            "propertyID": create_property().id,
            "dateTimeStart": Time.yesterday_iso(),
            "dateTimeEnd": Time.one_year_from_now_iso(),
        }

    yield _lease_payload


@pytest.fixture
def lease_attributes(faker):
    def _lease_attributes(unitNum, tenant, property, dateTimeStart, dateTimeEnd):
        return {
            **lease_attrs(faker, unitNum, dateTimeStart, dateTimeEnd),
            "tenantID": tenant.id,
            "propertyID": property.id,
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
        tenant = tenant or create_tenant()
        property = property or create_property()
        lease = LeaseModel.create(
            LeaseSchema,
            lease_attributes(unitNum, tenant, property, dateTimeStart, dateTimeEnd),
        )
        return lease

    yield _create_lease
