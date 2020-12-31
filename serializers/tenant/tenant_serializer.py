from schemas import TenantSchema


class TenantSerializer:
    @staticmethod
    def serialize(tenant):
        return TenantSchema().dump(tenant)
