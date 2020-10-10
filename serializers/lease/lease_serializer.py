from schemas import LeaseSchema


class LeaseSerializer:
    @staticmethod
    def serialize(lease):
        return LeaseSchema(exclude=("tenantID","propertyID")).dump(lease)
