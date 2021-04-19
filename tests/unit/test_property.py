import pytest
from tests.unit.base_interface_test import BaseInterfaceTest
from models.property import PropertyModel
from schemas.property import PropertySchema


class TestBasePropertyModel(BaseInterfaceTest):
    def setup(self):
        self.object = PropertyModel()
        self.custom_404_msg = "Property not found"
        self.schema = PropertySchema


@pytest.mark.usefixtures("empty_test_db")
class TestPropertyModel:
    def test_tenants(self, create_lease):
        lease = create_lease()
        property = lease.property
        tenant = lease.tenant

        assert property.tenants() == [tenant.json()]

    def test_json(self, create_property, create_property_manager, create_lease):
        manager_1 = create_property_manager()
        manager_2 = create_property_manager()
        property = create_property(manager_ids=[manager_1.id, manager_2.id])
        lease_1 = create_lease(property=property)
        lease_2 = create_lease(property=property)

        assert property.json() == {
            'id': property.id,
            'name': property.name,
            'address': property.address,
            'city': property.city,
            'state': property.state,
            'zipcode': property.zipcode,
            'num_units': property.num_units,
            'leases': [
                lease_1.json(),
                lease_2.json()
            ],
            'propertyManagers': [
                manager_1.json(),
                manager_2.json()
            ],
            'archived': property.archived,
        }
