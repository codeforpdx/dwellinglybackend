from schemas.emergency_contact import EmergencyContactSchema


class TestEmergencyContactValidations:
    def test_valid_payload(self, emergency_contact_attributes):
        valid_payload = emergency_contact_attributes
        no_validation_errors = {}

        assert no_validation_errors == EmergencyContactSchema().validate(valid_payload)

    def test_contact_numbers_cannot_be_empty(self):
        invalid_payload = {
            "name": "emergency contact name",
            "contact_numbers": [],
        }
        validation_errors = EmergencyContactSchema().validate(invalid_payload)

        assert "contact_numbers" in validation_errors

    def test_contact_numbers_required(self):
        invalid_payload = {
            "name": "emergency contact name",
        }
        validation_errors = EmergencyContactSchema().validate(invalid_payload)

        assert "contact_numbers" in validation_errors

    def test_multiple_contact_numbers_is_valid(
        self, emergency_contact_attributes, contact_number_attributes
    ):
        valid_payload = emergency_contact_attributes
        valid_payload["contact_numbers"].append(contact_number_attributes)

        no_validation_errors = {}

        assert no_validation_errors == EmergencyContactSchema().validate(valid_payload)
