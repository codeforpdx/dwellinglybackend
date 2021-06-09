import pytest
from schemas import TicketSchema


@pytest.mark.usefixtures("empty_test_db")
class TestTicketValidations:
    def test_valid_payload_without_note(self, create_tenant, create_admin_user):

        valid_payload = {
            "tenant_id": create_tenant().id,
            "author_id": create_admin_user().id,
        }

        no_validation_errors = {}
        assert no_validation_errors == TicketSchema().validate(valid_payload)

    def test_valid_payload_with_note(
        self, create_tenant, create_admin_user, create_note
    ):

        author_id = create_admin_user().id
        valid_payload = {
            "tenant_id": create_tenant().id,
            "author_id": author_id,
            "note": {**create_note().json(), "user_id": author_id},
        }

        del valid_payload["note"]["user"]

        no_validation_errors = {}
        assert no_validation_errors == TicketSchema().validate(valid_payload)
