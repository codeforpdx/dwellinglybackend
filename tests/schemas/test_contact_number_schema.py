import pytest
from schemas.contact_number import ContactNumberSchema
from utils.time import Time


class TestContactNumberValidation:
    def test_valid_payload(self, create_tenant, create_contact_number):
        valid_payload = {
            'id': create_tenant().id,
            'number': create_tenant().number,
            'numtype': create_contact_number().numtype,
            'extension': create_contact_number().extension,
            'created_at': Time.yesterday(),
            'updated_at': Time.today()
        }

        no_validation_errors = {}

        assert no_validation_errors == ContactNumberSchema().validate(valid_payload)