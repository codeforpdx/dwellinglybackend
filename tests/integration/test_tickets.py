import pytest
from conftest import is_valid
from models.tickets import TicketStatus

endpoint = "/api/tickets"
validID = 1
invalidID = 777


def test_tickets_GET_all(client, test_database, auth_headers):
    response = client.get(endpoint, headers=auth_headers["admin"])
    assert is_valid(response, 200)
    assert len(response.json["tickets"]) == 4
    assert len(response.json["tickets"][0]["notes"]) == 2
    assert len(response.json["tickets"][1]["notes"]) == 1
    assert len(response.json["tickets"][2]["notes"]) == 1
    assert len(response.json["tickets"][3]["notes"]) == 0


def test_tickets_GET_byTenant(client, test_database, auth_headers):
    response = client.get(f"{endpoint}?tenantID=1", headers=auth_headers["admin"])
    assert is_valid(response, 200)
    assert len(response.json["tickets"]) == 2
    assert response.json["tickets"][0]["tenantID"] == 1
    assert response.json["tickets"][1]["tenantID"] == 1


def test_tickets_GET_one(client, test_database, auth_headers):
    response = client.get(f"{endpoint}/{validID}", headers=auth_headers["admin"])
    assert is_valid(response, 200)
    assert response.json["id"] == 1
    assert response.json["issue"] == "The roof, the roof, the roof is on fire."
    assert response.json["tenant"] == "Renty McRenter"
    assert response.json["senderID"] == 1
    assert response.json["tenantID"] == 1
    assert response.json["assignedUserID"] == 4
    assert response.json["sender"] == "user1 tester"
    assert response.json["assigned"] == "Mr. Sir"
    assert response.json["status"] == TicketStatus.In_Progress
    assert response.json["urgency"] == "Low"
    assert len(response.json["notes"]) == 2
    assert response.json["notes"][0]["ticketid"] == 1
    assert response.json["notes"][0]["text"] == "Tenant has over 40 cats."
    assert response.json["notes"][0]["user"] == "user2 tester"
    assert response.json["notes"][1]["ticketid"] == 1
    assert response.json["notes"][1]["text"] == "Issue Resolved with phone call"
    assert response.json["notes"][1]["user"] == "user3 tester"

    response = client.get(f"{endpoint}/{invalidID}", headers=auth_headers["admin"])
    assert is_valid(response, 404)
    assert response.json == {"message": "Ticket not found"}


def test_tickets_PUT(client, auth_headers):
    updatedTicket = {
        "senderID": 2,
        "tenantID": 2,
        "assignedUserID": 3,
        "status": "In Progress",
        "urgency": "high",
        "issue": "Leaky pipe",
        "note": "Tenant has a service dog",
    }

    response = client.put(
        f"{endpoint}/{validID}", json=updatedTicket, headers=auth_headers["admin"]
    )

    assert is_valid(response, 200)
    assert response.json["issue"] == "Leaky pipe"
    assert response.json["tenant"] == "Soho Muless"
    assert response.json["senderID"] == 2
    assert response.json["tenantID"] == 2
    assert response.json["assignedUserID"] == 3
    assert response.json["sender"] == "user2 tester"
    assert response.json["assigned"] == "user3 tester"
    assert response.json["status"] == TicketStatus.In_Progress
    assert response.json["urgency"] == "high"
    # Ticket already had 2 notes to begin with - and with this PUT - it's +1
    assert len(response.json["notes"]) == 3
    assert response.json["notes"][2]["ticketid"] == 1
    assert response.json["notes"][2]["text"] == "Tenant has a service dog"
    assert response.json["notes"][2]["user"] == "user2 tester"

    # verify jwt only
    response = client.put(
        f"{endpoint}/{validID}", json=updatedTicket, headers=auth_headers["admin"]
    )
    assert is_valid(response, 200)

    response = client.put(
        f"{endpoint}/{invalidID}", json=updatedTicket, headers=auth_headers["admin"]
    )
    # NOT FOUND - Trying to update a non-existing ticket
    assert is_valid(response, 404)
    assert response.json == {"message": "Ticket not found"}


def test_tickets_POST(client, auth_headers):
    # UNAUTHORIZED - Missing Authorization Header
    response = client.post(f"{endpoint}")
    assert is_valid(response, 401)
    assert response.json == {"message": "Missing authorization header"}

    # Successful call
    response = client.post(
        f"{endpoint}", json={"ids": [validID]}, headers=auth_headers["admin"]
    )
    assert is_valid(response, 200)
    assert response.json == {"message": "Tickets successfully deleted"}


@pytest.mark.usefixtures("empty_test_db")
class TestFixtures:
    def test_create_ticket(self, create_ticket):
        ticket = create_ticket()
        assert ticket
