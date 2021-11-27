from schemas import TicketSchema


class TestTicketValidations:
    def test_valid_payload(self, create_tenant, create_admin_user):
        valid_payload = {
            "tenant_id": create_tenant().id,
            "author_id": create_admin_user().id,
        }

        no_validation_errors = {}
        assert no_validation_errors == TicketSchema().validate(valid_payload)

    def test_status_validation(self, ticket_attributes):
        no_validation_errors = {}
        payload = ticket_attributes()
        for status in ("New", "In Progress", "Closed"):
            payload["status"] = status
            assert no_validation_errors == TicketSchema().validate(payload)

        payload["status"] = "123456789"
        validation_errors = TicketSchema().validate(payload)
        assert "status" in validation_errors
