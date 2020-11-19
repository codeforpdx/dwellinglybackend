from schemas.emergency_contact import EmergencyContactSchema

class TestEmergencyContactValidations:
    def test_valid_payload(self, empty_test_db):
        valid_payload = {
            'name': 'emergency contact name',
            'contact_numbers': [{"number": "some number"}, {"number1" : "some other number"}]
        }

        no_validation_errors = {}

        assert no_validation_errors == EmergencyContactSchema().validate(valid_payload)
