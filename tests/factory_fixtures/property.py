import pytest
from models.property import PropertyModel
from schemas.property import PropertySchema


def property_attrs(faker, archived=False):
    return {
        "name": faker.unique.company(),
        "address": faker.address(),
        "city": faker.city(),
        "num_units": faker.random_int(min=1),
        "state": faker.state(),
        "zipcode": faker.postcode(),
        "archived": archived,
    }


@pytest.fixture
def property_attributes(faker, create_property_manager):
    def _property_attributes(archived=False, manager_ids=None):
        if manager_ids is None:
            manager_ids = [create_property_manager().id]
        return {
            **property_attrs(faker, archived),
            "propertyManagerIDs": manager_ids,
        }

    yield _property_attributes


@pytest.fixture
def create_property(property_attributes, **kwargs):
    def _create_property(**kwargs):
        property = PropertyModel.create(
            payload=property_attributes(**kwargs), schema=PropertySchema
        )
        return property

    yield _create_property
