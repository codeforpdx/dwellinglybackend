import pytest
from db import db
from models.tickets import TicketModel
from schemas.ticket import TicketSchema
from unittest.mock import patch


@pytest.mark.usefixtures("client_class")
class BaseConfig:
    endpoint = "/api/tickets"


class TestTicketGET(BaseConfig):
    def test_get(self, valid_header, create_ticket):
        ticket = create_ticket()
        response = self.client.get(f"{self.endpoint}/{ticket.id}", headers=valid_header)

        assert response.status_code == 200
        assert response.json == ticket.json()


class TestTicketPUT(BaseConfig):
    def test_update(self, valid_header, create_ticket):
        ticket = create_ticket()
        with patch.object(TicketModel, "update", return_value=ticket) as mock_update:
            response = self.client.put(
                f"{self.endpoint}/{ticket.id}",
                json={"hello": "world"},
                headers=valid_header,
            )

        mock_update.assert_called_once_with(
            schema=TicketSchema, payload={"hello": "world"}
        )

        assert response.status_code == 200
        assert response.json == ticket.json()


class TestTicketDELETE(BaseConfig):
    def test_delete(self, valid_header):
        with patch.object(TicketModel, "delete") as mock_delete:
            response = self.client.delete(f"{self.endpoint}/1", headers=valid_header)

        mock_delete.assert_called_once_with(1)
        assert response.status_code == 200
        assert response.json == {"message": "Ticket removed from database"}


class TestTicketsGET(BaseConfig):
    def test_tickets_get_all(self, valid_header, create_ticket):
        ticket_1 = create_ticket()
        ticket_2 = create_ticket()
        response = self.client.get(self.endpoint, headers=valid_header)

        assert response.status_code == 200
        # SQLite and Postgresql returns different orders. Just compare both orders
        assert response.json == {
            "tickets": [ticket_1.json(), ticket_2.json()]
        } or response.json == {"tickets": [ticket_2.json(), ticket_1.json()]}

    def test_tickets_get_by_tenant(self, valid_header, create_ticket):
        ticket_1 = create_ticket()
        create_ticket()
        create_ticket()

        response = self.client.get(
            f"{self.endpoint}?tenant_id={ticket_1.tenant.id}", headers=valid_header
        )

        assert response.status_code == 200
        assert response.json == {"tickets": [ticket_1.json()]}


class TestTicketsPOST(BaseConfig):
    def test_create_ticket(self, valid_header, ticket_attributes):
        new_ticket = ticket_attributes()

        with patch.object(TicketModel, "create") as mock_create:
            response = self.client.post(
                self.endpoint, json=new_ticket, headers=valid_header
            )

        mock_create.assert_called_once_with(schema=TicketSchema, payload=new_ticket)

        assert response.status_code == 201
        assert response.json == {"message": "Ticket successfully created"}


class TestTicketsDELETE(BaseConfig):
    def test_delete_many(self, valid_header, create_note):
        note_1 = create_note()
        note_2 = create_note()
        ticket_1 = note_1.ticket
        ticket_2 = note_2.ticket

        response = self.client.delete(
            self.endpoint,
            json={"ids": [ticket_1.id, ticket_2.id]},
            headers=valid_header,
        )
        db.session.rollback()

        assert response.status_code == 200
        assert response.json == {"message": "Tickets successfully deleted"}
        assert TicketModel.query.all() == []

    def test_delete_many_ignores_nonexistent_ids(self, valid_header, create_ticket):
        nonExistentTicketId = 999
        ticketsToDelete = [create_ticket().id, nonExistentTicketId]
        deleteIds = {"ids": ticketsToDelete}
        response = self.client.delete(
            self.endpoint, json=deleteIds, headers=valid_header
        )

        assert response.status_code == 200
        assert response.json == {"message": "Tickets successfully deleted"}

    def test_delete_many_requires_ids_field(self, valid_header):
        missingIds = {"notIds": [5]}
        response = self.client.delete(
            self.endpoint, json=missingIds, headers=valid_header
        )
        assert response.status_code == 400
        assert response.json == {"message": "Ticket IDs missing in request"}


class TestFixtures:
    def test_create_ticket(self, create_ticket):
        ticket = create_ticket()
        assert ticket
