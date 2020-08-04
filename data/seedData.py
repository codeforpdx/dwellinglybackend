from db import db
from models.user import UserModel
from models.property import PropertyModel
from models.tenant import TenantModel
from models.tickets import TicketModel
from models.notes import NotesModel
from models.revoked_tokens import RevokedTokensModel
from models.emergency_contact import EmergencyContactModel

def seedData():

    user = UserModel(email="user1@dwellingly.org", role="admin", firstName="user1", lastName="tester", password="1234", phone="555-555-5555", archived=0)
    db.session.add(user)
    user = UserModel(email="user2@dwellingly.org", role="admin", firstName="user2", lastName="tester", password="1234", phone="555-555-5555", archived=0)
    db.session.add(user)
    user = UserModel(email="user3@dwellingly.org", role="admin", firstName="user3", lastName="tester", password="1234", phone="555-555-5555", archived=0)
    db.session.add(user)
    user = UserModel(email="MisterSir@dwellingly.org", role="property-manager", firstName="Mr.", lastName="Sir", password="1234", phone="555-555-5555", archived=0)
    db.session.add(user)
    user = UserModel(email="user3@dwellingly.org", role="property-manager", firstName="Gray", lastName="Pouponn", password="1234", phone="555-555-5555", archived=0)
    db.session.add(user)
    db.session.commit()

    user = UserModel(email="pending1@dwellingly.org", role="pending", firstName="Anthony", lastName="Redding", password="1234", phone="555-555-5555", archived=0)
    db.session.add(user)
    user = UserModel(email="pending2@dwellingly.org", role="pending", firstName="Ryan", lastName="Dander", password="1234", phone="555-555-5555", archived=0)
    db.session.add(user)
    user = UserModel(email="pending3@dwellingly.org", role="pending", firstName="Amber", lastName="Lemming", password="1234", phone="555-555-5555", archived=0)
    db.session.add(user)
    user = UserModel(email="pending4@dwellingly.org", role="pending", firstName="Jeremy", lastName="Quazar", password="1234", phone="555-555-5555", archived=0)
    db.session.add(user)

    newProperty = PropertyModel(name="test1", address="123 NE FLanders St", city="Portland", state="OR", zipcode="97207", propertyManager=5, tenants=3, dateAdded="2020-04-12", archived=0)
    db.session.add(newProperty)
    newProperty = PropertyModel(name="Meerkat Manor", address="Privet Drive", city="Portland", state="OR", zipcode="97207", propertyManager=4, tenants=6, dateAdded="2020-04-12", archived=0)
    db.session.add(newProperty)
    newProperty = PropertyModel(name="The Reginald", address="Aristocrat Avenue", city="Portland", state="OR", zipcode="97207", propertyManager=5, tenants=4, dateAdded="2020-04-12", archived=0)
    db.session.add(newProperty)
    db.session.commit()

    newTenant = TenantModel(firstName="Renty", lastName="McRenter", phone="800-RENT-ALOT", propertyID=1, staffIDs=[1, 2])
    db.session.add(newTenant)
    newTenant = TenantModel(firstName="Soho", lastName="Muless", phone="123-123-0000", propertyID=2, staffIDs=[])
    db.session.add(newTenant)
    newTenant = TenantModel(firstName="Starvin", lastName="Artist", phone="123-123-1111", propertyID=2, staffIDs=[])
    db.session.add(newTenant)

    newNote = NotesModel(ticketid=0, text="Tenant not responding to phone calls.", user=1)
    db.session.add(newNote)
    newNote = NotesModel(ticketid=1, text="Tenant has over 40 cats.", user=2)
    db.session.add(newNote)
    newNote = NotesModel(ticketid=1, text="Issue Resolved with phone call", user=3)
    db.session.add(newNote)
    newNote = NotesModel(ticketid=2, text="Contacted Tenant -- follow up tomorrow.", user=3)
    db.session.add(newNote)

    newTicket = TicketModel(issue="The roof, the roof, the roof is one fire.", tenant=1, sender=1, status="In Progress", urgency="Low", assignedUser=4)
    db.session.add(newTicket)
    newTicket = TicketModel(issue="Flaming Dumpster Fire.", tenant=2, sender=3, status="Critical", urgency="HIGH", assignedUser=4)
    db.session.add(newTicket)
    newTicket = TicketModel(issue="Unpaid Rent", tenant=1, sender=1, status="Critical", urgency="HIGH", assignedUser=4)
    db.session.add(newTicket)
    newTicket = TicketModel(issue="Over 40 cats in domicile.", tenant=2, sender=3, status="Critical", urgency="HIGH", assignedUser=4)
    db.session.add(newTicket)

    revokedToken = RevokedTokensModel(jti="855c5cb8-c871-4a61-b3d8-90249f979601")
    db.session.add(revokedToken)

    emergencyContact = EmergencyContactModel(name="Narcotics Anonymous", contact_numbers=[{"number": "503-345-9839"}])
    db.session.add(emergencyContact)
    emergencyContact = EmergencyContactModel(name="Washington Co. Crisis Team", contact_numbers=[{"number": "503-291-9111", "numtype": "Call"}, {"number": "503-555-3321", "numtype": "Text"}], description="Suicide prevention and referrals")
    db.session.add(emergencyContact)
    emergencyContact = EmergencyContactModel(name="Child Abuse/Reporting", contact_numbers=[{"number": "503-730-3100"}])
    db.session.add(emergencyContact)

    db.session.commit()
