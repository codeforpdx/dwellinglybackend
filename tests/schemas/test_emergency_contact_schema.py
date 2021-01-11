import pytest
from schemas.emergency_contact import EmergencyContactSchema


@pytest.mark.usefixtures("empty_test_db")
class TestEmergencyContactValidations:
    def test_valid_payload(self):
        valid_payload = {
            "name": "emergency contact name",
            "contact_numbers": [{"number": "503-456-7890"}],
        }

        no_validation_errors = {}

        assert no_validation_errors == EmergencyContactSchema().validate(valid_payload)

    def test_validate_empty_contact_number(self):
        invalid_payload = {
            "name": "emergency contact name",
            "contact_numbers": [],
        }
        validation_errors = EmergencyContactSchema().validate(invalid_payload)

        assert "contact_numbers" in validation_errors

    def test_validate_missing_contact_numbers(self):
        invalid_payload = {
            "name": "emergency contact name",
        }
        validation_errors = EmergencyContactSchema().validate(invalid_payload)

        assert "contact_numbers" in validation_errors

    def test_validate_multiple_contact_numbers(self):
        valid_payload = {
            "name": "emergency contact name",
            "contact_numbers": [
                {"number": "503-291-9111", "numtype": "Call"},
                {"number": "503-555-3321", "numtype": "Text"},
            ],
        }
        no_validation_errors = {}

        assert no_validation_errors == EmergencyContactSchema().validate(valid_payload)

    def test_contact_num_too_long(self):
        invalid_payload = {
            "name": "emergency contact name",
            "contact_numbers": [{"number": "123-456-7890123456789"}],
        }
        validation_errors = EmergencyContactSchema().validate(invalid_payload)

        assert "contact_numbers" in validation_errors

    def test_contact_num_not_string(self):
        invalid_payload = {
            "name": "emergency contact name",
            "contact_numbers": [{"number": 503 - 123 - 4567}],
        }
        validation_errors = EmergencyContactSchema().validate(invalid_payload)

        assert "contact_numbers" in validation_errors
