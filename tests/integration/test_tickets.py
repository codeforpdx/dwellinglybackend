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
    response = client.get(f"{endpoint}?tenant_id=1", headers=auth_headers["admin"])
    assert is_valid(response, 200)
    assert len(response.json["tickets"]) == 2
    assert response.json["tickets"][0]["tenant_id"] == 1
    assert response.json["tickets"][1]["tenant_id"] == 1


def test_tickets_GET_one(client, test_database, auth_headers):
    response = client.get(f"{endpoint}/{validID}", headers=auth_headers["admin"])
    assert is_valid(response, 200)
    assert response.json["id"] == 1
    assert response.json["issue"] == "The roof, the roof, the roof is on fire."
    assert response.json["tenant"] == "Renty McRenter"
    assert response.json["author_id"] == 1
    assert response.json["tenant_id"] == 1
    assert response.json["sender"] == "user1 tester"
    assert response.json["status"] == TicketStatus.In_Progress
    assert response.json["urgency"] == "Low"
    assert len(response.json["notes"]) == 2
    assert response.json["notes"][0]["ticket_id"] == 1
    assert response.json["notes"][0]["text"] == "Tenant has over 40 cats."
    assert response.json["notes"][0]["user"] == "user2 tester"
    assert response.json["notes"][1]["ticket_id"] == 1
    assert response.json["notes"][1]["text"] == "Issue Resolved with phone call"
    assert response.json["notes"][1]["user"] == "user3 tester"

    response = client.get(f"{endpoint}/{invalidID}", headers=auth_headers["admin"])
    assert is_valid(response, 404)
    assert response.json == {"message": "Ticket not found"}


def test_tickets_POST(client, auth_headers):
    newTicket = {
        "author_id": 1,
        "tenant_id": 1,
        "status": "New",
        "urgency": "low",
        "issue": "Lead paint issue",
    }

    response = client.post(endpoint, json=newTicket, headers=auth_headers["admin"])

    assert is_valid(response, 201)
    assert response.json == {"message": "Ticket successfully created"}


def test_tickets_with_note_POST(client, auth_headers):
    newTicket = {
        "author_id": 1,
        "tenant_id": 1,
        "status": "New",
        "urgency": "low",
        "issue": "Lead paint issue",
        "notes": {"text": "note text", "user_id": 1, "ticket_id": 1},
    }

    response = client.post(endpoint, json=newTicket, headers=auth_headers["admin"])
    assert is_valid(response, 201)
    assert response.json == {"message": "Ticket successfully created"}


def test_tickets_PUT(client, auth_headers):
    updatedTicket = {
        "author_id": 2,
        "tenant_id": 2,
        "status": "In_Progress",
        "urgency": "high",
        "issue": "Leaky pipe",
    }

    response = client.put(
        f"{endpoint}/{validID}", json=updatedTicket, headers=auth_headers["admin"]
    )

    assert is_valid(response, 200)
    assert response.json["issue"] == "Leaky pipe"
    assert response.json["tenant"] == "Soho Muless"
    assert response.json["author_id"] == 2
    assert response.json["tenant_id"] == 2
    assert response.json["sender"] == "user2 tester"
    assert response.json["status"] == TicketStatus.In_Progress
    assert response.json["urgency"] == "high"

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


def test_tickets_DELETE(client, auth_headers, create_ticket):
    response = client.delete(f"{endpoint}/{validID}", headers=auth_headers["admin"])
    assert is_valid(response, 200)
    assert response.json == {"message": "Ticket removed from database"}

    response = client.delete(f"{endpoint}/{validID}", headers=auth_headers["admin"])
    # NOT FOUND - Trying to delete a non-existing ticket or an already deleted ticket
    assert is_valid(response, 404)
    assert response.json == {"message": "Ticket not found"}


def test_tickets_DELETE_list(client, auth_headers, create_ticket):
    ticketsToDelete = [create_ticket().id, create_ticket().id]
    deleteIds = {"ids": ticketsToDelete}
    response = client.delete(endpoint, json=deleteIds, headers=auth_headers["pm"])
    assert is_valid(response, 200)
    assert response.json == {"message": "Tickets successfully deleted"}

    nonExistentTicketId = 999
    ticketsToDelete = [create_ticket().id, nonExistentTicketId]
    deleteIds = {"ids": ticketsToDelete}
    response = client.delete(endpoint, json=deleteIds, headers=auth_headers["pm"])
    assert is_valid(response, 200)
    assert response.json == {"message": "Tickets successfully deleted"}

    missingIds = {"notIds": [5]}
    response = client.delete(endpoint, json=missingIds, headers=auth_headers["pm"])
    assert is_valid(response, 400)
    assert response.json == {"message": "Ticket IDs missing in request"}


@pytest.mark.usefixtures("empty_test_db")
class TestFixtures:
    def test_create_ticket(self, create_ticket):
        ticket = create_ticket()
        assert ticket
