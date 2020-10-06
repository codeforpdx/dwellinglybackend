from schemas import LeaseSchema


class LeaseSerializer:
    @staticmethod
    def serialize(lease):
        return LeaseSchema().dump(lease)
