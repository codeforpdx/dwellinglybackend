import pytest
from schemas.contact_number import ContactNumberSchema


@pytest.mark.usefixture("empty_test_db")
class TestContactNumberValidation:
    def test_valid_payload(self):
        valid_payload = {"number": "503-503-5031"}
        no_validation_errors = {}

        assert no_validation_errors == ContactNumberSchema().validate(valid_payload)

    def test_empty_payload(self):
        empty_payload = {}
        validation_errors = ContactNumberSchema().validate(empty_payload)

        assert "number" in validation_errors

    def test_invalid_payload(self):
        invalid_payload = {"number": None}
        validation_errors = ContactNumberSchema().validate(invalid_payload)

        assert "number" in validation_errors

    def test_contact_num_too_long(self):
        invalid_payload = {
            "number": "123-456-7890123456789",
        }
        validation_errors = ContactNumberSchema().validate(invalid_payload)

        assert "number" in validation_errors

    def test_contact_num_not_string(self):
        invalid_payload = {
            "number": 503 - 123 - 4567,
        }
        validation_errors = ContactNumberSchema().validate(invalid_payload)

        assert "number" in validation_errors
