import pytest
from schemas import TicketSchema


@pytest.mark.usefixtures("empty_test_db")
class TestTicketValidations:
    def test_valid_payload(self, create_tenant, create_admin_user):

        valid_payload = {
            "tenant_id": create_tenant().id,
            "creator_id": create_admin_user().id,
        }

        no_validation_errors = {}
        assert no_validation_errors == TicketSchema().validate(valid_payload)
