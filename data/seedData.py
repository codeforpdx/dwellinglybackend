from datetime import datetime, timedelta

from models.user import UserModel, RoleEnum
from models.property import PropertyModel
from models.tenant import TenantModel
from models.tickets import TicketModel, TicketStatus
from models.notes import NotesModel
from models.revoked_tokens import RevokedTokensModel
from models.emergency_contact import EmergencyContactModel
from models.contact_number import ContactNumberModel
from models.lease import LeaseModel
from schemas import PropertySchema, TenantSchema, UserRegisterSchema


def seedData():
    now = datetime.utcnow()
    future = now + timedelta(days=365)

    user_1 = UserModel(
        email="user1@dwellingly.org",
        role=RoleEnum.ADMIN,
        firstName="user1",
        lastName="tester",
        password="1234",
        phone="555-555-5555",
        archived=False,
    )
    user_1.save_to_db()
    user_2 = UserModel(
        email="user2@dwellingly.org",
        role=RoleEnum.ADMIN,
        firstName="user2",
        lastName="tester",
        password="1234",
        phone="555-555-5555",
        archived=False,
    )
    user_2.save_to_db()
    user_3 = UserModel(
        email="user3@dwellingly.org",
        role=RoleEnum.ADMIN,
        firstName="user3",
        lastName="tester",
        password="1234",
        phone="555-555-5555",
        archived=False,
    )
    user_3.save_to_db()
    user_mister_sir = UserModel(
        email="MisterSir@dwellingly.org",
        role=RoleEnum.PROPERTY_MANAGER,
        firstName="Mr.",
        lastName="Sir",
        password="1234",
        phone="555-555-5555",
        archived=False,
    )
    user_mister_sir.save_to_db()
    user_gray_pouponn = UserModel(
        email="GrayPouponn@dwellingly.org",
        role=RoleEnum.PROPERTY_MANAGER,
        firstName="Gray",
        lastName="Pouponn",
        password="1234",
        phone="555-555-5555",
        archived=False,
    )
    user_gray_pouponn.save_to_db()
    UserModel.create(
        payload={
            "email": "pending1@dwellingly.org",
            "firstName": "Anthony",
            "lastName": "Redding",
            "password": "1234",
            "phone": "555-555-5555",
        },
        schema=UserRegisterSchema,
    )
    UserModel.create(
        payload={
            "email": "pending2@dwellingly.org",
            "firstName": "Ryan",
            "lastName": "Dander",
            "password": "1234",
            "phone": "555-555-5555",
        },
        schema=UserRegisterSchema,
    )
    UserModel.create(
        payload={
            "email": "pending3@dwellingly.org",
            "firstName": "Amber",
            "lastName": "Lemming",
            "password": "1234",
            "phone": "555-555-5555",
        },
        schema=UserRegisterSchema,
    )
    UserModel.create(
        payload={
            "email": "pending4@dwellingly.org",
            "firstName": "Jeremy",
            "lastName": "Quazar",
            "password": "1234",
            "phone": "555-555-5555",
        },
        schema=UserRegisterSchema,
    )
    user_janice_joinstaff = UserModel(
        email="janice@joinpdx.org",
        role=RoleEnum.STAFF,
        firstName="Janice",
        lastName="Joinstaff",
        password="1234",
        phone="555-555-5555",
        archived=False,
    )
    user_janice_joinstaff.save_to_db()
    user_hector_chen = UserModel(
        email="hector@joinpdx.org",
        role=RoleEnum.STAFF,
        firstName="Hector",
        lastName="Chen",
        password="1234",
        phone="555-555-5555",
        archived=False,
    )
    user_hector_chen.save_to_db()
    user_xander_dander = UserModel(
        email="xander@joinpdx.org",
        role=RoleEnum.STAFF,
        firstName="Xander",
        lastName="Dander",
        password="1234",
        phone="555-555-5555",
        archived=False,
    )
    user_xander_dander.save_to_db()

    property_test1 = PropertyModel.create(
        payload={
            "name": "test1",
            "address": "123 NE FLanders St",
            "num_units": 5,
            "city": "Portland",
            "state": "OR",
            "zipcode": "97207",
            "propertyManagerIDs": [user_gray_pouponn.id],
        },
        schema=PropertySchema,
    )

    property_meerkat_manor = PropertyModel.create(
        payload={
            "name": "Meerkat Manor",
            "address": "Privet Drive",
            "num_units": 2,
            "city": "Portland",
            "state": "OR",
            "zipcode": "97207",
            "propertyManagerIDs": [user_mister_sir.id],
        },
        schema=PropertySchema,
    )

    property_the_reginald = PropertyModel.create(
        payload={
            "name": "The Reginald",
            "address": "Aristocrat Avenue",
            "num_units": 3,
            "city": "Portland",
            "state": "OR",
            "zipcode": "97207",
            "propertyManagerIDs": [user_gray_pouponn.id, user_mister_sir.id],
        },
        schema=PropertySchema,
    )

    tenant_renty_mcrenter = TenantModel.create(
        schema=TenantSchema,
        payload={
            "firstName": "Renty",
            "lastName": "McRenter",
            "phone": "800-RENT-ALOT",
            "staffIDs": [user_janice_joinstaff.id, user_hector_chen.id],
        },
    )

    tenant_soho_muless = TenantModel.create(
        schema=TenantSchema,
        payload={
            "firstName": "Soho",
            "lastName": "Muless",
            "phone": "123-123-0000",
            "staffIDs": [],
        },
    )

    tenant_starvin_artist = TenantModel.create(
        schema=TenantSchema,
        payload={
            "firstName": "Starvin",
            "lastName": "Artist",
            "phone": "123-123-1111",
            "staffIDs": [],
        },
    )

    ticket_roof_on_fire = TicketModel(
        issue="The roof, the roof, the roof is on fire.",
        tenantID=tenant_renty_mcrenter.id,
        senderID=user_1.id,
        status=TicketStatus.In_Progress,
        urgency="Low",
        assignedUserID=user_mister_sir.id,
    )
    ticket_roof_on_fire.save_to_db()
    ticket_dumpster_fire = TicketModel(
        issue="Flaming Dumpster Fire.",
        tenantID=tenant_soho_muless.id,
        senderID=user_3.id,
        status=TicketStatus.New,
        urgency="Critical",
        assignedUserID=user_mister_sir.id,
    )
    ticket_dumpster_fire.save_to_db()
    ticket_unpaid_rent = TicketModel(
        issue="Unpaid Rent",
        tenantID=tenant_renty_mcrenter.id,
        senderID=user_1.id,
        status=TicketStatus.New,
        urgency="High",
        assignedUserID=user_mister_sir.id,
    )
    ticket_unpaid_rent.save_to_db()
    ticket_40_cats = TicketModel(
        issue="Over 40 cats in domicile.",
        tenantID=tenant_soho_muless.id,
        senderID=user_3.id,
        status=TicketStatus.Closed,
        urgency="Low",
        assignedUserID=user_mister_sir.id,
    )
    ticket_40_cats.save_to_db()

    note_not_responding = NotesModel(
        ticketid=ticket_unpaid_rent.id,
        text="Tenant not responding to phone calls.",
        userid=user_1.id,
    )
    note_not_responding.save_to_db()
    note_over_40_cats = NotesModel(
        ticketid=ticket_roof_on_fire.id,
        text="Tenant has over 40 cats.",
        userid=user_2.id,
    )
    note_over_40_cats.save_to_db()
    note_issue_resolved = NotesModel(
        ticketid=ticket_roof_on_fire.id,
        text="Issue Resolved with phone call",
        userid=user_3.id,
    )
    note_issue_resolved.save_to_db()
    note_contacted_tenant = NotesModel(
        ticketid=ticket_dumpster_fire.id,
        text="Contacted Tenant -- follow up tomorrow.",
        userid=user_3.id,
    )
    note_contacted_tenant.save_to_db()

    RevokedTokensModel(jti="855c5cb8-c871-4a61-b3d8-90249f979601").save_to_db()

    EmergencyContactModel(
        name="Narcotics Anonymous",
        contact_numbers=[ContactNumberModel(number="503-345-9839")],
    ).save_to_db()

    EmergencyContactModel(
        name="Washington Co. Crisis Team",
        description="Suicide prevention and referrals",
        contact_numbers=[
            ContactNumberModel(number="503-291-9111", numtype="Call"),
            ContactNumberModel(number="503-555-3321", numtype="Text"),
        ],
    ).save_to_db()

    EmergencyContactModel(
        name="Child Abuse/Reporting",
        contact_numbers=[ContactNumberModel(number="503-730-3100")],
    ).save_to_db()

    lease_1 = LeaseModel(
        propertyID=property_test1.id,
        tenantID=tenant_renty_mcrenter.id,
        dateTimeStart=now,
        dateTimeEnd=future,
        occupants=3,
        unitNum="123",
    )
    lease_1.save_to_db()
    lease_2 = LeaseModel(
        propertyID=property_meerkat_manor.id,
        tenantID=tenant_soho_muless.id,
        dateTimeStart=now,
        dateTimeEnd=future,
        occupants=2,
        unitNum="418",
    )
    lease_2.save_to_db()
    lease_3 = LeaseModel(
        propertyID=property_the_reginald.id,
        tenantID=tenant_starvin_artist.id,
        dateTimeStart=now,
        dateTimeEnd=future,
        occupants=1,
        unitNum="D2",
    )
    lease_3.save_to_db()
