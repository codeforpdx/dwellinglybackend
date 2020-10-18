import pytest
from serializers.property import PropertySerializer
from utils.time import Time


@pytest.mark.usefixtures('empty_test_db')
class TestPropertySerializer:
    def test_serializer(self, create_property):
        property = create_property()

        assert PropertySerializer.serialize(property) == {
            'id': property.id,
            'name':property.name,
            'address': property.address,
            'unit': property.unit,
            'city': property.city,
            'state': property.state,
            'zipcode': property.zipcode,
            'archived': property.archived,
            'created_at': Time.serialized_date_format(property.created_at),
            'updated_at': None
        }
