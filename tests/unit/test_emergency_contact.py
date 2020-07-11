from conftest import emergency_contact_name, emergency_contact_description, contact_number, contact_numtype

#note: this test inherently tests the contact_number model as well

def test_emergency_contact(emergency_contact):
  assert emergency_contact.name == emergency_contact_name
  assert emergency_contact.description == emergency_contact_description
  assert emergency_contact.contact_numbers[0].number == contact_number
  assert emergency_contact.contact_numbers[0].numtype == contact_numtype


