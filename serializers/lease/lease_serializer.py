from schemas import LeaseSchema


class LeaseSerializer:
    @staticmethod
    def serialize(lease, many=False):
        return LeaseSchema(many=many, exclude=("tenantID", "propertyID")).dump(lease)
