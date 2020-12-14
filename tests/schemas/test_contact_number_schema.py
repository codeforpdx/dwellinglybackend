from schemas.contact_number import ContactNumberSchema


class TestContactNumberValidation:
    def test_valid_payload(self, empty_test_db):
        valid_payload = {
            "number": "503-503-503"
        }
        no_validation_errors = {}

        assert no_validation_errors == ContactNumberSchema().validate(valid_payload)
