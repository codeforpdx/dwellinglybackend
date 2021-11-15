import pytest
from models.tenant import TenantModel
from schemas.tenant import TenantSchema
from tests.attributes import tenant_attrs


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
def create_tenant(tenant_attributes, create_join_staff):
    def _create_tenant(staff=None):
        if isinstance(staff, int):
            staff = [create_join_staff().id for _ in range(staff)]
        elif staff is None:
            staff = []

        return TenantModel.create(
            schema=TenantSchema, payload=tenant_attributes(staff=staff)
        )

    yield _create_tenant
