from models.user import UserModel, RoleEnum
from unittest.mock import patch
import jwt
import time
from freezegun import freeze_time

@patch.object(jwt, 'encode')
def test_reset_password_token(stubbed_encode, app, test_database):
    user = UserModel.find_by_id(1)

    with freeze_time(time.ctime(time.time())):
        ten_minutes = time.time() + 600
        payload = {'user_id': user.id, 'exp': ten_minutes}

        assert user.reset_password_token()
        stubbed_encode.assert_called_once_with(payload, app.secret_key, algorithm='HS256')

def test_full_name():
    admin_user = UserModel(email=adminUserEmail, password="1234", firstName="first", lastName="last", phone=phone, role=adminRole, archived=0)
    assert admin_user.full_name() == 'first last'