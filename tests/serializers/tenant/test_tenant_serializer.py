from serializers.tenant import TenantSerializer
from utils.time import Time


class TestTenantSerializer:
    def test_serializer(self, create_tenant):
        tenant = create_tenant()

        assert TenantSerializer.serialize(tenant) == {
            "firstName": tenant.firstName,
            "id": tenant.id,
            "lastName": tenant.lastName,
            "phone": tenant.phone,
            "lease": None,
            "created_at": Time.format_date(tenant.created_at),
            "updated_at": Time.format_date(tenant.updated_at),
            "archived": tenant.archived,
        }
