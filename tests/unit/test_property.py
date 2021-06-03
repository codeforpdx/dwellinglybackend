import pytest
from tests.unit.base_interface_test import BaseInterfaceTest
from models.property import PropertyModel
from schemas.property import PropertySchema
from utils.time import Time
from dateutil.relativedelta import relativedelta


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
            "id": property.id,
            "name": property.name,
            "address": property.address,
            "city": property.city,
            "state": property.state,
            "zipcode": property.zipcode,
            "num_units": property.num_units,
            "leases": [lease_1.json(), lease_2.json()],
            "propertyManagers": [manager_1.json(), manager_2.json()],
            "archived": property.archived,
        }

    def test_json_with_tenants(self, create_property, create_lease):
        property = create_property()
        lease = create_lease(property=property)
        tenant = lease.tenant

        assert property.json(include_tenants=True)["tenants"] == [tenant.json()]

    def test_only_active_tenants_included(self, create_lease):
        active_lease = create_lease()

        old_lease_end = Time._yesterday()
        old_lease_start = old_lease_end - relativedelta(years=1)
        expired_lease = create_lease(
            property=active_lease.property,
            dateTimeStart=old_lease_start,
            dateTimeEnd=old_lease_end,
        )

        property = PropertyModel.find(expired_lease.propertyID)
        property_json = property.json(include_tenants=True)

        assert len(property_json["tenants"]) == 1
        assert len(property_json["leases"]) == 2
        assert active_lease.tenant.json() in property_json["tenants"]
        assert expired_lease.tenant.json() not in property_json["tenants"]
