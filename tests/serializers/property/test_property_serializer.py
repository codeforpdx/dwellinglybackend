from serializers.property import PropertySerializer
from utils.time import Time


class TestPropertySerializer:
    def test_serializer(self, create_property):
        property = create_property()

        assert PropertySerializer.serialize(property) == {
            "id": property.id,
            "name": property.name,
            "address": property.address,
            "num_units": property.num_units,
            "city": property.city,
            "state": property.state,
            "zipcode": property.zipcode,
            "archived": property.archived,
            "created_at": Time.format_date(property.created_at),
            "updated_at": Time.format_date(property.updated_at),
        }
