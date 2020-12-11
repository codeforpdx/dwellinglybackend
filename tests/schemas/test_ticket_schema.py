import pytest
from schemas import TicketSchema
from datetime import datetime
from utils.time import Time

class TestTicketValidations:
    def test_valid_payload(self, empty_test_db, create_tenant, create_admin_user, create_join_staff):

        valid_payload = {
            'tenantID': create_tenant().id,
            'assignedUserID': create_admin_user().id,
            'senderID': create_join_staff().id
        }

        no_validation_errors = {}
        assert no_validation_errors == TicketSchema().validate(valid_payload)