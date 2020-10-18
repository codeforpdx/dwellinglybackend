from db import db
from datetime import datetime, timedelta

from models.user import UserModel, RoleEnum
from models.property import PropertyModel
from models.tenant import TenantModel
from models.tickets import TicketModel
from models.notes import NotesModel
from models.revoked_tokens import RevokedTokensModel
from models.emergency_contact import EmergencyContactModel
from models.lease import LeaseModel
from utils.auth import hash_pw
from utils.time import time_format

hashed_password = hash_pw('1234')

def seedData():
    now=datetime.now()
    future = now + timedelta(days=365)

    user_1 = UserModel(email="user1@dwellingly.org",
                       role=RoleEnum.ADMIN,
                       firstName="user1",
                       lastName="tester",
                       password=hashed_password,
                       phone="555-555-5555",
                       archived=False)
    user_1.save_to_db()
    user_2 = UserModel(email="user2@dwellingly.org",
                       role=RoleEnum.ADMIN,
                       firstName="user2",
                       lastName="tester",
                       password=hashed_password,
                       phone="555-555-5555",
                       archived=False)
    user_2.save_to_db()
    user_3 = UserModel(email="user3@dwellingly.org",
                       role=RoleEnum.ADMIN,
                       firstName="user3",
                       lastName="tester",
                       password=hashed_password,
                       phone="555-555-5555",
                       archived=False)
    user_3.save_to_db()
    user_mister_sir = UserModel(email="MisterSir@dwellingly.org",
                                role=RoleEnum.PROPERTY_MANAGER,
                                firstName="Mr.",
                                lastName="Sir",
                                password=hashed_password,
                                phone="555-555-5555",
                                archived=False)
    user_mister_sir.save_to_db()
    user_gray_pouponn = UserModel(email="GrayPouponn@dwellingly.org",
                                  role=RoleEnum.PROPERTY_MANAGER,
                                  firstName="Gray",
                                  lastName="Pouponn",
                                  password=hashed_password,
                                  phone="555-555-5555",
                                  archived=False)
    user_gray_pouponn.save_to_db()

    user_anthony_redding = UserModel(email="pending1@dwellingly.org",
                                     role=RoleEnum.PENDING,
                                     firstName="Anthony",
                                     lastName="Redding",
                                     password=hashed_password,
                                     phone="555-555-5555",
                                     archived=False)
    user_anthony_redding.save_to_db()
    user_ryan_dander = UserModel(email="pending2@dwellingly.org",
                                 role=RoleEnum.PENDING,
                                 firstName="Ryan",
                                 lastName="Dander",
                                 password=hashed_password,
                                 phone="555-555-5555",
                                 archived=False)
    user_ryan_dander.save_to_db()
    user_amber_lemming = UserModel(email="pending3@dwellingly.org",
                                   role=RoleEnum.PENDING,
                                   firstName="Amber",
                                   lastName="Lemming",
                                   password=hashed_password,
                                   phone="555-555-5555",
                                   archived=False)
    user_amber_lemming.save_to_db()
    user_jeremy_quazar = UserModel(email="pending4@dwellingly.org",
                                   role=RoleEnum.PENDING,
                                   firstName="Jeremy",
                                   lastName="Quazar",
                                   password=hashed_password,
                                   phone="555-555-5555",
                                   archived=False)
    user_jeremy_quazar.save_to_db()
    user_janice_joinstaff = UserModel(email="janice@joinpdx.org",
                                      role=RoleEnum.STAFF,
                                      firstName="Janice",
                                      lastName="Joinstaff",
                                      password=hashed_password,
                                      phone="555-555-5555",
                                      archived=False)
    user_janice_joinstaff.save_to_db()
    user_hector_chen = UserModel(email="hector@joinpdx.org",
                                 role=RoleEnum.STAFF,
                                 firstName="Hector",
                                 lastName="Chen",
                                 password=hashed_password,
                                 phone="555-555-5555",
                                 archived=False)
    user_hector_chen.save_to_db()
    user_xander_dander = UserModel(email="xander@joinpdx.org",
                                   role=RoleEnum.STAFF,
                                   firstName="Xander",
                                   lastName="Dander",
                                   password=hashed_password,
                                   phone="555-555-5555",
                                   archived=False)
    user_xander_dander.save_to_db()

    property_test1 = PropertyModel(name="test1",
                                   address="123 NE FLanders St",
                                   unit="5",
                                   city="Portland",
                                   state="OR",
                                   zipcode="97207",
                                   propertyManager=user_gray_pouponn.id,
                                   archived=False)
    property_test1.save_to_db()
    property_meerkat_manor = PropertyModel(name="Meerkat Manor",
                                           address="Privet Drive",
                                           unit="2",
                                           city="Portland",
                                           state="OR",
                                           zipcode="97207",
                                           propertyManager=user_mister_sir.id,
                                           archived=False)
    property_meerkat_manor.save_to_db()
    property_the_reginald = PropertyModel(name="The Reginald",
                                          address="Aristocrat Avenue",
                                          unit="3",
                                          city="Portland",
                                          state="OR",
                                          zipcode="97207",
                                          propertyManager=user_gray_pouponn.id,
                                          archived=False)
    property_the_reginald.save_to_db()

    tenant_renty_mcrenter = TenantModel(firstName="Renty",
                                        lastName="McRenter",
                                        phone="800-RENT-ALOT",
                                        propertyID=property_test1.id,
                                        staffIDs=[user_1.id, user_2.id],
                                        unitNum=1)
    tenant_renty_mcrenter.save_to_db()
    tenant_soho_muless = TenantModel(firstName="Soho",
                                     lastName="Muless",
                                     phone="123-123-0000",
                                     propertyID=property_meerkat_manor.id,
                                     staffIDs=[],
                                     unitNum=2)
    tenant_soho_muless.save_to_db()
    tenant_starvin_artist = TenantModel(firstName="Starvin",
                                        lastName="Artist",
                                        phone="123-123-1111",
                                        propertyID=property_meerkat_manor.id,
                                        staffIDs=[],
                                        unitNum=3)
    tenant_starvin_artist.save_to_db()

    ticket_roof_on_fire = TicketModel(
        issue="The roof, the roof, the roof is on fire.",
        tenant=tenant_renty_mcrenter.id,
        sender=user_1.id,
        status="In Progress",
        urgency="Low",
        assignedUser=user_mister_sir.id)
    ticket_roof_on_fire.save_to_db()
    ticket_dumpster_fire = TicketModel(issue="Flaming Dumpster Fire.",
                                       tenant=tenant_soho_muless.id,
                                       sender=user_3.id,
                                       status="New",
                                       urgency="Critical",
                                       assignedUser=user_mister_sir.id)
    ticket_dumpster_fire.save_to_db()
    ticket_unpaid_rent = TicketModel(issue="Unpaid Rent",
                                     tenant=tenant_renty_mcrenter.id,
                                     sender=user_1.id,
                                     status="New",
                                     urgency="High",
                                     assignedUser=user_mister_sir.id)
    ticket_unpaid_rent.save_to_db()
    ticket_40_cats = TicketModel(issue="Over 40 cats in domicile.",
                                 tenant=tenant_soho_muless.id,
                                 sender=user_3.id,
                                 status="Closed",
                                 urgency="Low",
                                 assignedUser=user_mister_sir.id)
    ticket_40_cats.save_to_db()

    note_not_responding = NotesModel(
        0,
        text="Tenant not responding to phone calls.",
        user=user_1.id)
    note_not_responding.save_to_db()
    note_over_40_cats = NotesModel(ticketid=ticket_roof_on_fire.id,
                                   text="Tenant has over 40 cats.",
                                   user=user_2.id)
    note_over_40_cats.save_to_db()
    note_issue_resolved = NotesModel(ticketid=ticket_roof_on_fire.id,
                                     text="Issue Resolved with phone call",
                                     user=user_3.id)
    note_issue_resolved.save_to_db()
    note_contacted_tenant = NotesModel(
        ticketid=ticket_dumpster_fire.id,
        text="Contacted Tenant -- follow up tomorrow.",
        user=user_3.id)
    note_contacted_tenant.save_to_db()

    RevokedTokensModel(jti="855c5cb8-c871-4a61-b3d8-90249f979601").save_to_db()

    EmergencyContactModel(name="Narcotics Anonymous",
                          contact_numbers=[{
                              "number": "503-345-9839"
                          }]).save_to_db()
    EmergencyContactModel(
        name="Washington Co. Crisis Team",
        contact_numbers=[{
            "number": "503-291-9111",
            "numtype": "Call"
        }, {
            "number": "503-555-3321",
            "numtype": "Text"
        }],
        description="Suicide prevention and referrals").save_to_db()
    EmergencyContactModel(name="Child Abuse/Reporting",
                          contact_numbers=[{
                              "number": "503-730-3100"
                          }]).save_to_db()

    lease_1 = LeaseModel(name="Lease 1",
                         propertyID=property_test1.id,
                         tenantID=tenant_renty_mcrenter.id,
                         dateTimeStart=now,
                         dateTimeEnd=future,
                         occupants=3)
    lease_1.save_to_db()
    lease_2 = LeaseModel(name="Lease 2",
                         propertyID=property_meerkat_manor.id,
                         tenantID=tenant_soho_muless.id,
                         dateTimeStart=now,
                         dateTimeEnd=future,
                         occupants=2)
    lease_2.save_to_db()
    lease_3 = LeaseModel(name="Lease 3",
                         propertyID=property_the_reginald.id,
                         tenantID=tenant_starvin_artist.id,
                         dateTimeStart=now,
                         dateTimeEnd=future,
                         occupants=1)
    lease_3.save_to_db()

    try:
        db.session.commit()
    except:
        print("Error updating database")

    print("Database sucessfully seeded: " + now.strftime(time_format))
