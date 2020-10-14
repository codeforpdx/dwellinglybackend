import pytest
from models.property import PropertyModel

@pytest.fixture
def create_property(create_property_manager):
    def _create_property(pm=create_property_manager()):
        property = PropertyModel(
                name='the heights',
                address='111 SW Harrison',
                city="Portland",
                unit="101",
                state="OR",
                zipcode="97207",
                propertyManagerIDs=[pm.id],
                dateAdded="2020-04-12",
                archived=False
            )
        property.save_to_db()
        return property
    yield _create_property
