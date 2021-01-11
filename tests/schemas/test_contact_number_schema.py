from schemas.contact_number import ContactNumberSchema


class TestContactNumberValidation:
    def test_valid_payload(self, empty_test_db):
        valid_payload = {"number": "503-503-503"}
        no_validation_errors = {}

        assert no_validation_errors == ContactNumberSchema().validate(valid_payload)

    def test_empty_payload(self, empty_test_db):
        empty_payload = {}
        validation_errors = ContactNumberSchema().validate(empty_payload)

        assert "number" in validation_errors

    def test_invalid_payload(self, empty_test_db):
        invalid_payload = {"number": None}
        validation_errors = ContactNumberSchema().validate(invalid_payload)

        assert "number" in validation_errors
