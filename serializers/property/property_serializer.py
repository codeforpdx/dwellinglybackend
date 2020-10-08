from schemas import PropertySchema


class PropertySerializer:
    @staticmethod
    def serialize(property):
        return PropertySchema().dump(property)
