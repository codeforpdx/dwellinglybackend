import pytest
from schemas.user import *


class UserSchemaValidations:
    def test_unique_email(self, empty_test_db, create_join_staff):
        user = create_join_staff()

        payload = {
            'email': user.email
        }

        validation_errors = UserSchema().validate(payload)

        assert 'email' in validation_errors
        assert validation_errors['email'] == [f"A user with email '{user.email}' already exists"]


class TestUserValidations(UserSchemaValidations):
    pass


class TestUserRegisterSchemaValidations(UserSchemaValidations):
    def test_presence_of_role_key_is_not_valid(self):
        payload = {'role': 'ADMIN'}

        validation_errors = UserRegisterSchema().validate(payload)

        assert 'role' in validation_errors
        assert validation_errors['role'] == ['Role is not allowed']

    def test_password_is_required(self):
        validation_errors = UserRegisterSchema().validate({})

        assert 'password' in validation_errors
