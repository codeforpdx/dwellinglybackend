from models.lease import LeaseModel
from tests.time import Time
from models.user import UserModel
from models.property import PropertyModel
from models.tenant import TenantModel

def test_json(test_database):
    lease = LeaseModel.find_by_id(1)
    property = PropertyModel.find_by_id(lease.propertyID)
    landlord = UserModel.find_by_id(lease.landlordID)
    tenant = TenantModel.find_by_id(lease.tenantID)

    assert lease.json() == {
            'id': lease.id,
            'name': lease.name,
            'propertyID': property.json(),
            'landlordID': landlord.json(),
            'tenantID': tenant.json(),
            'dateTimeStart': Time.format_date(lease.dateTimeStart),
            'dateTimeEnd': Time.format_date(lease.dateTimeEnd),
            'dateUpdated': Time.format_date(lease.dateUpdated),
            'occupants': lease.occupants
        }
