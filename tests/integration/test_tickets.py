from conftest import is_valid

endpoint = '/api/tickets'


def test_tickets_GET_all(client, test_database, auth_headers):
    response = client.get(endpoint, headers=auth_headers["admin"])
    assert is_valid(response, 200)
    assert len(response.json['tickets']) == 4
    assert response.json['tickets'][0]['issue'] == 'The roof, the roof, the roof is one fire.'
    assert response.json['tickets'][0]['status'] == 'In Progress'


def test_tickets_GET_one(client, test_database, auth_headers):
    validID = 1
    response = client.get(f'{endpoint}/{validID}', headers=auth_headers["admin"])
    assert is_valid(response, 200)
    assert response.json['id'] == 1
    assert response.json['tenant'] == 'Renty McRenter'

    invalidID = 777
    response = client.get(f'{endpoint}/{invalidID}', headers=auth_headers["admin"])
    assert is_valid(response, 404)
