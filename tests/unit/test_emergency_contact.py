import pytest
from models.emergency_contact import EmergencyContactModel

emergency_contact_name = "Washington Co. Crisis Team"
emergency_contact_description = "Suicide prevention and referrals"
contact_number = "503-291-9111"
contact_numtype = "Call"

def test_emergency_contact(app):
  """The properties must match the model's inputs."""
  with app.app_context():
    emergency_contact = EmergencyContactModel(name=emergency_contact_name, contact_numbers=[{"number": contact_number, "numtype": contact_numtype}], description=emergency_contact_description)
    assert emergency_contact.name == emergency_contact_name
    assert emergency_contact.description == emergency_contact_description
    assert emergency_contact.contact_numbers[0].number == contact_number
    assert emergency_contact.contact_numbers[0].numtype == contact_numtype


@pytest.mark.usefixtures("empty_test_db")
class TestFixtures:
    def test_create_emergency_contact(self, create_emergency_contact):
        assert create_emergency_contact()
        