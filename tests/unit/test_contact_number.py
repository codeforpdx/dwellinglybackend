import pytest
from models.contact_number import ContactNumberModel

emergency_contact_id = 1
number = "503-291-9111"
numtype = "Call"
extension = "356"

def test_contact_number():
  contact_number = ContactNumberModel(emergency_contact_id, number, numtype, extension)
  assert contact_number.emergency_contact_id == emergency_contact_id
  assert contact_number.number == number
  assert contact_number.numtype == numtype
  assert contact_number.extension == extension


@pytest.mark.usefixtures("empty_test_db")
class TestFixtures:
    def test_create_contact_number(self, create_contact_number):
        assert create_contact_number()
        