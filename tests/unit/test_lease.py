import pytest
from tests.unit.base_interface_test import BaseInterfaceTest
from models.lease import LeaseModel
from schemas.lease import LeaseSchema
from tests.time import Time
from models.property import PropertyModel


class TestBaseLeaseModel(BaseInterfaceTest):
    def setup(self):
        self.object = LeaseModel()
        self.custom_404_msg = 'Lease not found'
        self.schema = LeaseSchema()

@pytest.mark.usefixtures('empty_test_db')
class TestLeaseModel():
    def test_json(self, create_lease):
        lease = create_lease()
        property = PropertyModel.find_by_id(lease.propertyID)

        assert lease.json() == {
                'id': lease.id,
                'name': lease.name,
                'propertyID': property.json(),
                'tenantID': lease.tenant.json(),
                'dateTimeStart': Time.format_date(lease.dateTimeStart),
                'dateTimeEnd': Time.format_date(lease.dateTimeEnd),
                'occupants': lease.occupants
            }
