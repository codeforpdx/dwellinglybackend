import pytest
from models.tenant import TenantModel
from schemas.tenant import TenantSchema


def tenant_attrs(faker):
    return {
        "firstName": faker.first_name(),
        "lastName": faker.last_name(),
        "phone": faker.phone_number(),
    }


@pytest.fixture
def tenant_attributes(faker, create_join_staff):
    def _tenant_attributes(staff=None):
        if staff is None:
            staff = [create_join_staff().id]
        return {
            **tenant_attrs(faker),
            "staffIDs": staff,
        }

    yield _tenant_attributes


@pytest.fixture
def create_tenant(tenant_attributes):
    def _create_tenant():
        return TenantModel.create(
            schema=TenantSchema, payload=tenant_attributes(staff=[])
        )

    yield _create_tenant
