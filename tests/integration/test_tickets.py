from conftest import is_valid
from datetime import datetime

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


def test_tickets_POST(client, auth_headers):
    newTicket = {
        'sender': 1,
        'tenant': 1,
        'status': 'new',
        'urgency': 'low',
        'issue': 'Lead paint issue',
        'note': [],
        "assignedUser": 4,
    }

    response = client.post(endpoint, json=newTicket, headers=auth_headers["admin"])
    assert is_valid(response, 201)
    assert response.json['id'] != 0
    assert response.json['issue'] == 'Lead paint issue'
    assert response.json['tenant'] == 'Renty McRenter'
    assert response.json['senderID'] == 1
    assert response.json['tenantID'] == 1
    assert response.json['assignedUserID'] == 4
    assert response.json['sender'] == 'user1 tester'
    assert response.json['assigned'] == 'Mr. Sir'
    assert response.json['status'] == 'new'
    assert response.json['urgency'] == 'low'
    assert response.json['opened'] == datetime.now().strftime("%d-%b-%Y (%H:%M)")
    assert response.json['updated'] == datetime.now().strftime("%d-%b-%Y (%H:%M)")
    assert response.json['notes'] == []
