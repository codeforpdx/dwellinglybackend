from conftest import is_valid

endpoint = "/api/tickets"
validTicketID = 1
invalidTicketID = 777


def test_notes_POST(client, auth_headers):
    newNote = {"text": "We don't need no water", "authorID": 5}

    response = client.post(
        f"{endpoint}/{validTicketID}/notes", json=newNote, headers=auth_headers["admin"]
    )

    assert is_valid(response, 200)
    assert response.json["id"] != 0
    assert response.json["issue"] == "The roof, the roof, the roof is on fire."
    assert response.json["tenant"] == "Renty McRenter"
    assert response.json["senderID"] == 1
    assert response.json["tenantID"] == 1
    assert response.json["status"] == "In Progress"
    assert response.json["assignedUserID"] == 4
    assert response.json["notes"][2]["id"] == 5
    assert response.json["notes"][2]["ticketid"] == 1
    assert response.json["notes"][2]["text"] == "We don't need no water"
    assert response.json["notes"][2]["user"] == "Gray Pouponn"

    response = client.post(
        f"{endpoint}/{invalidTicketID}/notes",
        json=newNote,
        headers=auth_headers["admin"],
    )

    assert is_valid(response, 404)  # NOT FOUND - 'Ticket not found'
