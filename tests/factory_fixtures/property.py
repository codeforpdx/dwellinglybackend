import pytest
from models.property import PropertyModel

@pytest.fixture
def property_attributes(faker):
    def _property_attributes(archived=False):
        return {
            'name': faker.unique.name(),
            'address': faker.address(),
            'city': faker.city(),
            'unit': faker.building_number(),
            'state': faker.state() ,
            'zipcode': faker.postcode(),
            'archived': archived,
        }
    yield _property_attributes

@pytest.fixture
def create_property(property_attributes, create_property_manager):
    def _create_property():
        property = PropertyModel(**property_attributes())
        property.managers = [create_property_manager()]
        property.save_to_db()
        return property
    yield _create_property
