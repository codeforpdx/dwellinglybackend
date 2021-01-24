from schemas.contact_number import ContactNumberSchema


class TestContactNumberValidation:
    def test_valid_payload(self, contact_number_attributes):
        valid_payload = contact_number_attributes
        no_validation_errors = {}

        assert no_validation_errors == ContactNumberSchema().validate(valid_payload)

    def test_empty_payload_is_invalid(self):
        empty_payload = {}
        validation_errors = ContactNumberSchema().validate(empty_payload)

        assert "number" in validation_errors

    def test_number_cannot_be_null(self):
        invalid_payload = {"number": None}
        validation_errors = ContactNumberSchema().validate(invalid_payload)

        assert "number" in validation_errors

    def test_number_cannot_exceed_max_length(self):
        invalid_payload = {
            "number": "8" * 50,
        }
        validation_errors = ContactNumberSchema().validate(invalid_payload)

        assert "number" in validation_errors
