from tests.unit.base_interface_test import BaseInterfaceTest
from models.property import PropertyModel
from schemas.property import PropertySchema


class TestBasePropertyModel(BaseInterfaceTest):
    def setup(self):
        self.object = PropertyModel()
        self.custom_404_msg = "Property not found"
        self.schema = PropertySchema

    def test_tenants_attached_to_property(self, create_lease):
        lease = create_lease()
        property_with_lease = PropertyModel.find_by_id(lease.propertyID)
        assert property_with_lease is not None
        assert property_with_lease.tenants() == [lease.tenant.json()]
