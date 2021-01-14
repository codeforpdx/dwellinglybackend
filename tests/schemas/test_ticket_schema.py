from schemas import TicketSchema


class TestTicketValidations:
    def test_valid_payload(
        self, empty_test_db, create_tenant, create_admin_user, create_join_staff
    ):

        valid_payload = {
            "tenantID": create_tenant().id,
            "assignedUserID": create_join_staff().id,
            "senderID": create_admin_user().id,
        }

        no_validation_errors = {}
        assert no_validation_errors == TicketSchema().validate(valid_payload)

    def test_assign_non_staff(
        self, empty_test_db, create_tenant, create_admin_user, create_join_staff
    ):
        invalid_assigned_user = {
            "tenantID": create_tenant().id,
            "assignedUserID": create_admin_user().id,
            "senderID": create_join_staff().id,
        }

        validation_errors = TicketSchema().validate(invalid_assigned_user)
        assert "assignedUserID" in validation_errors
