from schemas.user import UserSchema, UserRegisterSchema
from models.user import RoleEnum, UserType


def user_register_valid_payload(user):
    return {
        "firstName": user["firstName"],
        "lastName": user["lastName"],
        "phone": user["phone"],
        "email": user["email"],
        "password": user["password"],
    }


class UserSchemaValidations:
    def test_unique_email(self, empty_test_db, create_join_staff):
        user = create_join_staff()

        payload = {"email": user.email}

        validation_errors = self.schema().validate(payload)

        assert "email" in validation_errors
        assert validation_errors["email"] == [
            f"A user with email '{user.email}' already exists"
        ]

    def test_role_enum_validation(self):
        user_schema = UserSchema()
        payload = {"role": 999}
        validation_error = user_schema.validate(payload)
        assert "role" in validation_error
        assert validation_error["role"] == ["Invalid role"]

        payload = {"role": "STAFF"}
        validation_error = user_schema.validate(payload)
        assert "role" in validation_error
        assert validation_error["role"] == ["Invalid role"]

        payload = {"role": RoleEnum.STAFF.value}
        no_validation_error = user_schema.validate(payload)
        assert "role" not in no_validation_error

    def test_role_enum_serialization(self, empty_test_db, create_join_staff):
        user = create_join_staff()
        user_schema = UserSchema()
        user_serialized = user_schema.dump(user)
        user_serialized["role"] = user.role.value


class TestUserSchemaValidations(UserSchemaValidations):
    def setup(self):
        self.schema = UserSchema


class TestInheritedUserRegisterSchemaValidations(UserSchemaValidations):
    def setup(self):
        self.schema = UserRegisterSchema


class TestUserRegisterSchemaValidations:
    def test_user_register_valid_payload(self, empty_test_db, user_attributes):
        no_validation_errors = {}

        assert no_validation_errors == UserRegisterSchema().validate(
            user_register_valid_payload(user_attributes())
        )

    def test_presence_of_role_key_is_not_valid(self):
        payload = {"role": RoleEnum.ADMIN.value}

        validation_errors = UserRegisterSchema().validate(payload)

        assert "role" in validation_errors
        assert validation_errors["role"] == ["Role is not allowed"]

    def test_presence_of_type_is_not_valid(self):
        payload = {"type": UserType.ADMIN.value}

        validation_errors = UserRegisterSchema().validate(payload)

        assert "type" in validation_errors
        assert validation_errors["type"] == ["Type is not allowed"]

    def test_password_is_required(self):
        validation_errors = UserRegisterSchema().validate({})

        assert "password" in validation_errors
