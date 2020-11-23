import pytest
from schemas import UserSchema


class TestUserValidations:
    def test_valid_payload(self, empty_test_db, create_property_manager):
        valid_payload = {
            'email': create_property_manager().email
        }

        no_validation_errors = {}

        assert no_validation_errors == UserSchema().validate(valid_payload)
