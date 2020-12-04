import pytest
from schemas import TicketSchema
from datetime import datetime
from utils.time import Time

class TestTicketValidations:
    def test_valid_payload(self, empty_test_db, create_tenant, create_admin_user, create_join_staff):

        valid_payload = {
            'tenantID': create_tenant().id,
            'assignedUser': create_admin_user().id,
            'sender': create_join_staff().id
        }

        no_validation_errors = {}
        assert no_validation_errors == TicketSchema().validate(valid_payload)