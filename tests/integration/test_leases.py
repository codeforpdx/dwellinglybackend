import pytest
from freezegun import freeze_time
from conftest import is_valid
from models.user import UserModel
from models.property import PropertyModel
from models.lease import LeaseModel
from models.tenant import TenantModel
from tests.time import Time


@pytest.mark.usefixtures('client_class', 'test_database')
class TestGetLease:
    def setup(self):
        self.endpoint = '/api/lease'
        self.lease = LeaseModel.find_by_id(1)
        self.property = PropertyModel.find_by_id(self.lease.propertyID)
        self.landlord = UserModel.find_by_id(self.lease.landlordID)
        self.tenant = TenantModel.find_by_id(self.lease.tenantID)

    def test_authorized_request_for_a_lease(self, auth_headers):
        response = self.client.get(
                f'{self.endpoint}/{self.lease.id}',
                headers=auth_headers["pm"]
            )

        assert is_valid(response, 200)
        assert response.json == {
            'id': self.lease.id,
            'name': self.lease.name,
            'propertyID': self.property.json(),
            'landlordID': self.landlord.json(),
            'tenantID': self.tenant.json(),
            'dateTimeStart': Time.format_date(self.lease.dateTimeStart),
            'dateTimeEnd': Time.format_date(self.lease.dateTimeEnd),
            'dateUpdated': Time.format_date(self.lease.dateUpdated),
            'occupants': self.lease.occupants
        }

    def test_authorized_request_for_a_non_existent_lease(self, auth_headers):
        response = self.client.get(
                f'{self.endpoint}/504',
                headers=auth_headers["pm"]
            )

        assert is_valid(response, 404)
        assert response.json == {'Message': 'Lease Not Found'}

    def test_unauthorized_request_for_a_lease(self):
        response = self.client.get(f'{self.endpoint}/{self.lease.id}')
    
        assert is_valid(response, 401)
        assert response.json == {'msg': 'Missing Authorization Header'}

    def test_authorized_request_for_all_leases(self, auth_headers):
        lease_2 = LeaseModel.find_by_id(2)
        property_2 = PropertyModel.find_by_id(lease_2.propertyID)
        landlord_2 = UserModel.find_by_id(lease_2.landlordID)
        tenant_2 = TenantModel.find_by_id(lease_2.tenantID)

        lease_3 = LeaseModel.find_by_id(3)
        property_3 = PropertyModel.find_by_id(lease_3.propertyID)
        landlord_3 = UserModel.find_by_id(lease_3.landlordID)
        tenant_3 = TenantModel.find_by_id(lease_3.tenantID)

        response = self.client.get(self.endpoint, headers=auth_headers["pm"])
    
        assert is_valid(response, 200)
        assert response.json == {
                "Leases": [
                    {
                        'id': self.lease.id,
                        'name': self.lease.name,
                        'propertyID': self.property.json(),
                        'landlordID': self.landlord.json(),
                        'tenantID': self.tenant.json(),
                        'dateTimeStart': Time.format_date(self.lease.dateTimeStart),
                        'dateTimeEnd': Time.format_date(self.lease.dateTimeEnd),
                        'dateUpdated': Time.format_date(self.lease.dateUpdated),
                        'occupants': self.lease.occupants
                    },
                    {
                        'id': lease_2.id,
                        'name': lease_2.name,
                        'propertyID': property_2.json(),
                        'landlordID': landlord_2.json(),
                        'tenantID': tenant_2.json(),
                        'dateTimeStart': Time.format_date(lease_2.dateTimeStart),
                        'dateTimeEnd': Time.format_date(lease_2.dateTimeEnd),
                        'dateUpdated': Time.format_date(lease_2.dateUpdated),
                        'occupants': lease_2.occupants
                    },
                    {
                        'id': lease_3.id,
                        'name': lease_3.name,
                        'propertyID': property_3.json(),
                        'landlordID': landlord_3.json(),
                        'tenantID': tenant_3.json(),
                        'dateTimeStart': Time.format_date(lease_3.dateTimeStart),
                        'dateTimeEnd': Time.format_date(lease_3.dateTimeEnd),
                        'dateUpdated': Time.format_date(lease_3.dateUpdated),
                        'occupants': lease_3.occupants
                    }
                ]
            }
 
    def test_unauthorized_request_for_all_leases(self):
        response = self.client.get(self.endpoint)
    
        assert is_valid(response, 401)
        assert response.json == {'msg': 'Missing Authorization Header'}


@pytest.mark.usefixtures('client_class', 'test_database')
class TestCreateLease:
    def setup(self):
        self.endpoint = '/api/lease'

        self.valid_payload = {
                'dateTimeStart': Time.today(),
                'dateTimeEnd': Time.one_year_from_now()
            }
        self.invalid_payload = {}

    def test_authorized_request_with_valid_payload(self, auth_headers):
        num_leases = len(LeaseModel.query.all())
        response = self.client.post(self.endpoint, json=self.valid_payload, headers=auth_headers["pm"])

        assert is_valid(response, 200)
        assert response.json == 201
        assert num_leases + 1 == len(LeaseModel.query.all())

    def test_unauthorized_request_with_valid_payload(self):
        response = self.client.post(self.endpoint, json=self.valid_payload)
    
        assert is_valid(response, 401)
        assert response.json == {'msg': 'Missing Authorization Header'}

    def test_authorized_request_with_invalid_payload(self, auth_headers):
        with pytest.raises(TypeError):
            response = self.client.post(self.endpoint, json=self.invalid_payload, headers=auth_headers["pm"])


@pytest.mark.usefixtures('client_class', 'test_database')
class TestDeleteLease:
    def setup(self):
        self.endpoint = '/api/lease'
        self.lease = LeaseModel.find_by_id(1)

    def test_authorized_request_with_valid_lease_id(self, auth_headers):
        num_leases = len(LeaseModel.query.all())
        response = self.client.delete(f'{self.endpoint}/1', headers=auth_headers["pm"])

        assert is_valid(response, 200)
        assert response.json == {'Message': 'Lease Removed from Database'}
        assert num_leases - 1 == len(LeaseModel.query.all())

    def test_authorized_request_with_invalid_lease_id(self, auth_headers):
        num_leases = len(LeaseModel.query.all())
        response = self.client.delete(f'{self.endpoint}/504', headers=auth_headers["pm"])

        assert is_valid(response, 200)
        assert response.json == {'Message': 'Lease Removed from Database'}
        assert num_leases == len(LeaseModel.query.all())


@pytest.mark.usefixtures('client_class', 'test_database')
class TestUpdateLease:
    def setup(self):
        self.endpoint = '/api/lease'
        self.lease = LeaseModel.find_by_id(1)

    def test_valid_lease_id(self, auth_headers):
        response = self.client.put(f'{self.endpoint}/{self.lease.id}', headers=auth_headers["pm"])

        assert is_valid(response, 201)
        assert response.json == self.lease.json()

    def test_invalid_lease_id(self, auth_headers):
        response = self.client.put(f'{self.endpoint}/504', headers=auth_headers["pm"])

        assert is_valid(response, 404)
        assert response.json == {'Message': 'Lease Not Found'}

    def test_date_is_updated_with_valid_payload(self, auth_headers):
        payload = {'dateTimeEnd': Time.one_year_from_now()}
        old_date = Time.format_date(self.lease.dateUpdated)

        with freeze_time(Time.one_year_from_now()):
            response = self.client.put(f'{self.endpoint}/{self.lease.id}', json=payload, headers=auth_headers["pm"])
            
            assert is_valid(response, 201)
            assert response.json['dateUpdated'] != old_date

    def test_updatedDate_is_left_unchanged_when_given_invalid_params(self, auth_headers):
        old_date = Time.format_date(self.lease.dateUpdated)

        with freeze_time(Time.one_year_from_now()):
            response = self.client.put(f'{self.endpoint}/{self.lease.id}', json={}, headers=auth_headers["pm"])

        assert is_valid(response, 201)
        assert response.json['dateUpdated'] == old_date
        
    def test_invalid_attribute_ids(self, auth_headers):
        payload = {
                'name': 'I',
                'landlordID': '504',
                'propertyID': '504',
                'tenantID': '504',
                'occupants': '504',
                'dateTimeStart': Time.one_year_from_now(),
                'dateTimeEnd': Time.today()
            }

        with pytest.raises(AttributeError):
            response = self.client.put(f'{self.endpoint}/{self.lease.id}', json=payload, headers=auth_headers["pm"])

    def test_valid_attrs_are_all_updated(self, auth_headers):
        start_date = Time.one_year_from_now()
        end_date = Time.today()
        payload = {
                'name': 'I',
                'landlordID': '2',
                'propertyID': '2',
                'tenantID': '2',
                'occupants': '200',
                'dateTimeStart': start_date,
                'dateTimeEnd': end_date
            }

        response = self.client.put(f'{self.endpoint}/{self.lease.id}', json=payload, headers=auth_headers["pm"])

        assert is_valid(response, 201)
        assert response.json['name'] == 'I'
        assert response.json['landlordID']['id'] == 2
        assert response.json['propertyID']['id'] == 2
        assert response.json['tenantID']['id'] == 2
        assert response.json['occupants'] == 200
        assert response.json['dateTimeStart'] == start_date
        assert response.json['dateTimeEnd'] == end_date
        assert response.json == self.lease.json()


@pytest.mark.usefixtures('client_class', 'test_database')
class TestLeaseAuthorizations:
    # Test auth is in place at each endpoint
    def test_unauthorized_get_request(self):
        response = self.client.get('/api/lease/1')
    
        assert is_valid(response, 401)
        assert response.json == {'msg': 'Missing Authorization Header'}

    def test_unauthorized_get_all_request(self):
        response = self.client.get('/api/lease')
    
        assert is_valid(response, 401)
        assert response.json == {'msg': 'Missing Authorization Header'}

    def test_unauthorized_create_request(self):
        response = self.client.post('/api/lease')
    
        assert is_valid(response, 401)
        assert response.json == {'msg': 'Missing Authorization Header'}

    def test_unauthorized_delete_request(self):
        response = self.client.delete('/api/lease/1')
    
        assert is_valid(response, 401)
        assert response.json == {'msg': 'Missing Authorization Header'}

    def test_unauthorized_update_request(self):
        response = self.client.put('/api/lease/1')
    
        assert is_valid(response, 401)
        assert response.json == {'msg': 'Missing Authorization Header'}

    # Test all roles are authorized to access each endpoint
    def test_authorized_get_request(self, auth_headers):
        for _, role in auth_headers.items():
            response = self.client.get('/api/lease/1', headers=role)
            assert is_valid(response, 200)

    def test_authorized_get_all_request(self, auth_headers):
        for _, role in auth_headers.items():
            response = self.client.get('/api/lease', headers=role)
            assert is_valid(response, 200)

    def test_authorized_create_request(self, auth_headers):
        payload = {
                'dateTimeStart': Time.today(),
                'dateTimeEnd': Time.one_year_from_now()
            }
        for _, role in auth_headers.items():
            response = self.client.post('/api/lease', json=payload, headers=role)
            assert is_valid(response, 200)

    def test_authorized_delete_request(self, auth_headers):
        for _, role in auth_headers.items():
            response = self.client.delete('/api/lease/1', headers=role)
            assert is_valid(response, 200)

    def test_authorized_update_request(self, auth_headers):
        for _, role in auth_headers.items():
            response = self.client.put('/api/lease/1', headers=role)
            assert is_valid(response, 201)
