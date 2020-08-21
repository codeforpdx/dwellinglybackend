from conftest import is_valid
from datetime import datetime

endpoint = '/api/tickets'
validID = 1
invalidID = 777


def test_tickets_GET_all(client, test_database, auth_headers):
    response = client.get(endpoint, headers=auth_headers["admin"])
    assert is_valid(response, 200)
    assert len(response.json['tickets']) == 4
    assert len(response.json['tickets'][0]['notes']) == 2
    assert len(response.json['tickets'][1]['notes']) == 1
    assert len(response.json['tickets'][2]['notes']) == 0
    assert len(response.json['tickets'][3]['notes']) == 0


def test_tickets_GET_one(client, test_database, auth_headers):
    response = client.get(f'{endpoint}/{validID}', headers=auth_headers["admin"])
    assert is_valid(response, 200)
    assert response.json['id'] == 1
    assert response.json['issue'] == 'The roof, the roof, the roof is one fire.'
    assert response.json['tenant'] == 'Renty McRenter'
    assert response.json['senderID'] == 1
    assert response.json['tenantID'] == 1
    assert response.json['assignedUserID'] == 4
    assert response.json['sender'] == 'user1 tester'
    assert response.json['assigned'] == 'Mr. Sir'
    assert response.json['status'] == 'In Progress'
    assert response.json['urgency'] == 'Low'
    assert len(response.json['notes']) == 2
    assert response.json['notes'][0]['ticketid'] == 1
    assert response.json['notes'][0]['text'] == 'Tenant has over 40 cats.'
    assert response.json['notes'][0]['user'] == 'user2 tester'
    assert response.json['notes'][1]['ticketid'] == 1
    assert response.json['notes'][1]['text'] == 'Issue Resolved with phone call'
    assert response.json['notes'][1]['user'] == 'user3 tester'

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


def test_tickets_PUT(client, auth_headers):
    updatedTicket = {
        'sender': 2,
        'tenant': 2,
        'assignedUser': 3,
        'status': 'in progress',
        'urgency': 'high',
        'issue': 'Leaky pipe',
    }
    response = client.put(f'{endpoint}/{validID}', json=updatedTicket, headers=auth_headers["admin"])
    assert is_valid(response, 200)
    assert response.json['issue'] == 'Leaky pipe'
    assert response.json['tenant'] == 'Soho Muless'
    assert response.json['senderID'] == 2
    assert response.json['tenantID'] == 2
    assert response.json['assignedUserID'] == 3
    assert response.json['sender'] == 'user2 tester'
    assert response.json['assigned'] == 'user3 tester'
    assert response.json['status'] == 'in progress'
    assert response.json['urgency'] == 'high'
    assert response.json['updated'] == datetime.now().strftime("%d-%b-%Y (%H:%M)")
    assert len(response.json['notes']) == 2


def test_tickets_DELETE(client, auth_headers):

    response = client.delete(f'{endpoint}/{validID}')
    # UNAUTHORIZED - Missing Authorization Header
    assert is_valid(response, 401)

    response = client.delete(f'{endpoint}/{invalidID}', headers=auth_headers["admin"])
    assert is_valid(response, 200)
