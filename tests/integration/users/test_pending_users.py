import pytest
from freezegun import freeze_time
from utils.time import Time, time_format
from datetime import datetime


@pytest.mark.usefixtures("empty_test_db")
class TestPendingUsers:
    def test_users_pending(self, client, valid_header, create_unauthorized_user):
        pending_user = create_unauthorized_user()
        assert pending_user.lastActive.strftime(time_format) != "01/01/2020 00:00:00"

        with freeze_time("2020-01-01"):
            """The get pending users returns one user with no role
            and a successful response code."""
            response = client.get(
                "/api/users/pending",
                headers=valid_header,
            )
            print("################# RESPONSE ISS")
            print(response.get_json())

            expected_time = Time.format_date_by_year(datetime.now())
            # created_at = fields.DateTime(time_format)

            print("################# TIME IS")
            print(expected_time)

            # expected_response = {'users': [
            #                                 {
            #                                 'id': 2,
            #                                 'firstName': 'Amy',
            #                                 'lastName': 'Roberts',
            #                                 'email': 'john51@gmail.com',
            #                                 'phone': '965-934-2320',
            #                                 'role': None,
            #                                 'archived': False,
            #                                 'lastActive':
            #                                 '02/18/2021 03:27:53',
            #                                 'created_at':
            #                                 '02/18/2021 03:27:53',
            #                                 'updated_at':
            #                                 '02/18/2021 03:27:53'
            #                                 }
            #                                 ]}

            assert len(response.get_json()["users"]) == 1
            assert response.status_code == 200
            # TODO What we want to test here is that we get back the expected
            #  json response, not the length of the response. We want to assert
            #  the actual response so that we can be confident that we are returning
            #  the correct data to the frontend.


# TODO We need a test for the endpoint that checks the actual json response is what
#  we expect it to be.


# def test_last_active(client, test_database, admin_user):
#     user = UserModel.find_by_email(admin_user.email)
#     assert user.lastActive.strftime(time_format) != "01/01/2020 00:00:00"
#
#     with freeze_time("2020-01-01"):
#         client.post(
#             "/api/login",
#             json={"email": admin_user.email, "password": plaintext_password},
#         )
#         user = UserModel.find_by_email(admin_user.email)
#         assert user.lastActive.strftime(time_format) == "01/01/2020 00:00:00"
