from schemas.emergency_contact import EmergencyContactSchema


#TODO: Write a test for validation methods and for properties being validated correctly
class TestEmergencyContactValidations:
    def test_valid_payload(self, empty_test_db):
        valid_payload = {
            'name': 'emergency contact name',
            'contact_numbers': [{"number": "some number"}]
        }

        no_validation_errors = {}

        assert no_validation_errors == EmergencyContactSchema().validate(valid_payload)
