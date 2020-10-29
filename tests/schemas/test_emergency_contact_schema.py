import pytest

from schemas.emergency_contact import EmergencyContactSchema
from utils.time import Time


class TestEmergencyContactValidations:
    def test_valid_payload(self, create_tenant, create_property):
        valid_payload = {
            'id': create_tenant().id,
            'name': create_tenant().firstName + " " + create_tenant().lastName,
            'description': "home",
            'contact_numbers': ["90312345678", "9031112222", "9999999999"],
            'created_at': Time.format_date(Time.yesterday()),
            'updated_at': Time.format_date(Time.today())
        }

        no_validation_errors = {}

        assert no_validation_errors == EmergencyContactSchema().validate(valid_payload)
