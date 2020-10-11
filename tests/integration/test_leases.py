import pytest
from conftest import is_valid
from models.lease import LeaseModel
from tests.time import Time

def valid_payload(tenant_id):
    return {
            'dateTimeStart': Time.today(),
            'dateTimeEnd': Time.one_year_from_now(),
            'tenantID': tenant_id
        }


@pytest.mark.usefixtures('client_class', 'empty_test_db')
class TestLease:
    def setup(self):
        self.endpoint = '/api/lease'

    def test_get_a_lease(self, valid_header, create_lease):
        lease = create_lease()

        response = self.client.get(
                f'{self.endpoint}/{lease.id}',
                headers=valid_header
            )

        assert is_valid(response, 200)
        assert response.json == lease.json()

    def test_get_all_leases(self, valid_header, create_lease):
        lease = create_lease()
        another_lease = create_lease(name='World')

        response = self.client.get(self.endpoint, headers=valid_header)

        assert is_valid(response, 200)
        assert response.json == {
                "Leases": [
                    lease.json(),
                    another_lease.json()
                ]
            }

    def test_create_lease(self, valid_header, create_tenant):
        response = self.client.post(
            '/api/lease',
            json=valid_payload(create_tenant().id),
            headers=valid_header
        )

        assert is_valid(response, 201)
        assert response.json == {'message': 'Lease created successfully'}

    def test_delete_lease(self, valid_header, create_lease):
        lease = create_lease()

        response = self.client.delete(f'/api/lease/{lease.id}', headers=valid_header)

        assert is_valid(response, 200)
        assert response.json == {'message': 'Lease deleted'}

    def test_update_lease(self, valid_header, create_lease):
        lease = create_lease()
        response = self.client.put(
            f'/api/lease/{lease.id}',
            json={'name': 'I'},
            headers=valid_header
        )

        assert is_valid(response, 200)
        assert response.json['name'] == 'I'


@pytest.mark.usefixtures('client_class', 'empty_test_db')
class TestLeaseAuthorizations:
    # Test auth is in place at each endpoint
    def test_unauthorized_get_request(self):
        response = self.client.get('/api/lease/1')

        assert is_valid(response, 401)
        assert response.json == {'message': 'Missing authorization header'}

    def test_unauthorized_get_all_request(self):
        response = self.client.get('/api/lease')

        assert is_valid(response, 401)
        assert response.json == {'message': 'Missing authorization header'}

    def test_unauthorized_create_request(self):
        response = self.client.post('/api/lease')

        assert is_valid(response, 401)
        assert response.json == {'message': 'Missing authorization header'}

    def test_unauthorized_delete_request(self):
        response = self.client.delete('/api/lease/1')

        assert is_valid(response, 401)
        assert response.json == {'message': 'Missing authorization header'}

    def test_unauthorized_update_request(self):
        response = self.client.put('/api/lease/1')

        assert is_valid(response, 401)
        assert response.json == {'message': 'Missing authorization header'}

    # Test all roles are authorized to access each endpoint
    def test_pm_authorized_to_get(self, pm_header, create_lease):
        lease = create_lease()

        response = self.client.get(f'/api/lease/{lease.id}', headers=pm_header)
        assert is_valid(response, 200)

    def test_staff_are_authorized_to_get(self, staff_header, create_lease):
        lease = create_lease()

        response = self.client.get(f'/api/lease/{lease.id}', headers=staff_header)
        assert is_valid(response, 200)

    def test_admin_is_authorized_to_get(self, admin_header, create_lease):
        lease = create_lease()

        response = self.client.get(f'/api/lease/{lease.id}', headers=admin_header)
        assert is_valid(response, 200)

    def test_pm_is_authorized_to_get_all(self, pm_header, create_lease):
        lease = create_lease()

        response = self.client.get('/api/lease', headers=pm_header)
        assert is_valid(response, 200)

    def test_staff_are_authorized_to_get_all(self, staff_header, create_lease):
        lease = create_lease()

        response = self.client.get('/api/lease', headers=staff_header)
        assert is_valid(response, 200)

    def test_admin_is_authorized_to_get_all(self, admin_header, create_lease):
        lease = create_lease()

        response = self.client.get('/api/lease', headers=admin_header)
        assert is_valid(response, 200)

    def test_pm_is_authorized_to_create(self, pm_header, create_tenant):
        response = self.client.post('/api/lease', json=valid_payload(create_tenant().id), headers=pm_header)

        assert is_valid(response, 201)

    def test_staff_are_authorized_to_create(self, staff_header, create_tenant):
        response = self.client.post('/api/lease', json=valid_payload(create_tenant().id), headers=staff_header)
        assert is_valid(response, 201)

    def test_admin_is_authorized_to_create(self, admin_header, create_tenant):
        response = self.client.post('/api/lease', json=valid_payload(create_tenant().id), headers=admin_header)
        assert is_valid(response, 201)

    def test_pm_is_authorized_to_delete_lease(self, pm_header, create_lease):
        lease = create_lease()
        response = self.client.delete(f'/api/lease/{lease.id}'.format(id), headers=pm_header)

        assert is_valid(response, 200)

    def test_staff_are_authorized_to_delete_lease(self, staff_header, create_lease):
        lease = create_lease()
        response = self.client.delete(f'/api/lease/{lease.id}'.format(id), headers=staff_header)

        assert is_valid(response, 200)

    def test_admin_is_authorized_to_delete_lease(self, admin_header, create_lease):
        lease = create_lease()
        response = self.client.delete(f'/api/lease/{lease.id}'.format(id), headers=admin_header)

        assert is_valid(response, 200)

    def test_pm_is_authorized_to_update(self, pm_header, create_lease):
        lease = create_lease()
        payload = {
                'dateTimeStart': Time.today(),
                'dateTimeEnd': Time.one_year_from_now()
            }
        response = self.client.put(f'/api/lease/{lease.id}', json=payload, headers=pm_header)
        assert is_valid(response, 200)

    def test_staff_authorized_to_update(self, staff_header, create_lease):
        lease = create_lease()
        payload = {
                'dateTimeStart': Time.today(),
                'dateTimeEnd': Time.one_year_from_now()
            }
        response = self.client.put(f'/api/lease/{lease.id}', json=payload, headers=staff_header)
        assert is_valid(response, 200)

    def test_admin_authorized_to_update(self, admin_header, create_lease):
        lease = create_lease()
        payload = {
                'dateTimeStart': Time.today(),
                'dateTimeEnd': Time.one_year_from_now()
            }
        response = self.client.put(f'/api/lease/{lease.id}', json=payload, headers=admin_header)
        assert is_valid(response, 200)
