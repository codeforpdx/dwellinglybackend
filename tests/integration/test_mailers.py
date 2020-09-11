import pytest
from conftest import is_valid
from unittest.mock import patch
from flask_mail import Mail


@pytest.mark.usefixtures('client_class', 'test_database')
class TestPostEmail:
    def setup(self):
        self.endpoint = '/api/user/message'

    @patch.object(Mail, 'send')
    def test_email_can_be_sent(self, stubbed_send, auth_headers):
        payload = {
                'userid': 1,
                'title': 'Some email subject',
                'body': 'Some body'
            }
        
        response = self.client.post(
                f'{self.endpoint}',
                json=payload,
                headers=auth_headers["admin"]
            )
        assert is_valid(response, 200)
        stubbed_send.assert_called()
