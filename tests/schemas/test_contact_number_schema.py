import pytest
from schemas.contact_number import ContactNumberSchema
from utils.time import Time


class TestContactNumberValidation:
    def test_valid_payload(self, create_tenant, create_property):
        valid_payload = {
            'id': create_tenant().id,
            'number': create_tenant().number,
            'numtype': "home",
            'extension': "ext",
            'created_at': Time.format_date(Time.yesterday()),
            'updated_at': Time.format_date(Time.today())
        }

        no_validation_errors = {}

        assert no_validation_errors == ContactNumberSchema().validate(valid_payload)