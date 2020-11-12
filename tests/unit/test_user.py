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

def test_full_name(empty_test_db, create_admin_user):
    admin= create_admin_user(firstName='first', lastName='last')
    assert admin.full_name() == 'first last'
