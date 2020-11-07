import pytest

from schemas.emergency_contact import EmergencyContactSchema

#TODO: Write a test for validation methods and for properties being validated correctly
class TestEmergencyContactValidations:
    def test_valid_payload(self, create_emergency_contact):
        valid_payload = {
            'name': create_emergency_contact().firstName,
            'description': create_emergency_contact().description,
            'contact_numbers': create_emergency_contact().contact_numbers
        }

        no_validation_errors = {}

        assert no_validation_errors == EmergencyContactSchema().validate(valid_payload)
