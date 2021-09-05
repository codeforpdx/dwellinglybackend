# Seed file for generating fake data for development.
#
# The seed file is not used within the context of the flask framework
# All models that are explicitly and implicitly used need to be loaded.
# Flake 8 will throw F401 errors in this file. Need to ignore them otherwise
# implicit imports in models will fail to load.
#

from models.user import UserModel, RoleEnum
from models.users.admin import Admin
from models.users.staff import Staff
from models.users.property_manager import PropertyManager
from models.property import PropertyModel
from models.tenant import TenantModel
from models.tickets import TicketModel, TicketStatus
from models.notes import NotesModel
from models.emergency_contact import EmergencyContactModel
from models.contact_number import ContactNumberModel  # noqa: F401
from models.lease import LeaseModel
from schemas import *  # noqa: F403
from utils.time import Time
from faker import Faker


def seed():
    faker = Faker()

    admin = Admin.create(
        schema=UserSchema,
        payload={
            "email": "user1@dwellingly.org",
            "role": RoleEnum.ADMIN.value,
            "firstName": "user1",
            "lastName": "tester",
            "password": "1234",
            "phone": "555-555-5555",
        },
    )

    # Create some admins
    for _ in range(7):
        Admin.create(
            schema=UserSchema, payload=user_attributes(faker, role=RoleEnum.ADMIN.value)
        )

    # Create some archived admins
    for _ in range(2):
        Admin.create(
            schema=UserSchema,
            payload=user_attributes(faker, role=RoleEnum.ADMIN.value, archived=True),
        )

    user_2 = Admin.create(
        payload={
            "email": "user2@dwellingly.org",
            "role": RoleEnum.ADMIN.value,
            "firstName": "user2",
            "lastName": "tester",
            "password": "1234",
            "phone": "555-555-5555",
        },
        schema=UserSchema,
    )
    user_3 = Admin.create(
        payload={
            "email": "user3@dwellingly.org",
            "role": RoleEnum.ADMIN.value,
            "firstName": "user3",
            "lastName": "tester",
            "password": "1234",
            "phone": "555-555-5555",
        },
        schema=UserSchema,
    )
    user_mister_sir = PropertyManager.create(
        payload={
            "email": "MisterSir@dwellingly.org",
            "role": RoleEnum.PROPERTY_MANAGER.value,
            "firstName": "Mr.",
            "lastName": "Sir",
            "password": "1234",
            "phone": "555-555-5555",
        },
        schema=UserSchema,
    )
    user_gray_pouponn = PropertyManager.create(
        payload={
            "email": "GrayPouponn@dwellingly.org",
            "role": RoleEnum.PROPERTY_MANAGER.value,
            "firstName": "Gray",
            "lastName": "Pouponn",
            "password": "1234",
            "phone": "555-555-5555",
        },
        schema=UserSchema,
    )

    # Create some pending users
    for _ in range(5):
        UserModel.create(schema=UserRegisterSchema, payload=user_attributes(faker))

    # Create some archived users that were never approved.
    for _ in range(3):
        UserModel.create(
            schema=UserRegisterSchema, payload=user_attributes(faker, archived=True)
        )

    user_janice_joinstaff = Staff.create(
        payload={
            "email": "janice@joinpdx.org",
            "role": RoleEnum.STAFF.value,
            "firstName": "Janice",
            "lastName": "Joinstaff",
            "password": "1234",
            "phone": "555-555-5555",
        },
        schema=UserSchema,
    )
    user_hector_chen = Staff.create(
        payload={
            "email": "hector@joinpdx.org",
            "role": RoleEnum.STAFF.value,
            "firstName": "Hector",
            "lastName": "Chen",
            "password": "1234",
            "phone": "555-555-5555",
        },
        schema=UserSchema,
    )
    Staff.create(
        payload={
            "email": "xander@joinpdx.org",
            "role": RoleEnum.STAFF.value,
            "firstName": "Xander",
            "lastName": "Dander",
            "password": "1234",
            "phone": "555-555-5555",
        },
        schema=UserSchema,
    )

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

    ticket_roof_on_fire = TicketModel.create(
        schema=TicketSchema,
        payload={
            "issue": "The roof, the roof, the roof is on fire.",
            "tenant_id": tenant_renty_mcrenter.id,
            "author_id": admin.id,
            "status": TicketStatus.In_Progress.name,
            "urgency": "Low",
        },
    )
    ticket_dumpster_fire = TicketModel.create(
        schema=TicketSchema,
        payload={
            "issue": "Flaming Dumpster Fire.",
            "tenant_id": tenant_soho_muless.id,
            "author_id": user_3.id,
            "status": TicketStatus.New,
            "urgency": "Critical",
        },
    )
    ticket_unpaid_rent = TicketModel.create(
        schema=TicketSchema,
        payload={
            "issue": "Unpaid Rent",
            "tenant_id": tenant_renty_mcrenter.id,
            "author_id": admin.id,
            "status": TicketStatus.New,
            "urgency": "High",
        },
    )
    TicketModel.create(
        schema=TicketSchema,
        payload={
            "issue": "Over 40 cats in domicile.",
            "tenant_id": tenant_soho_muless.id,
            "author_id": user_3.id,
            "status": TicketStatus.Closed,
            "urgency": "Low",
        },
    )

    NotesModel.create(
        schema=NotesSchema,
        payload={
            "ticket_id": ticket_unpaid_rent.id,
            "text": "Tenant not responding to phone calls.",
            "user_id": admin.id,
        },
    )
    NotesModel.create(
        schema=NotesSchema,
        payload={
            "ticket_id": ticket_roof_on_fire.id,
            "text": "Tenant has over 40 cats.",
            "user_id": user_2.id,
        },
    )
    NotesModel.create(
        schema=NotesSchema,
        payload={
            "ticket_id": ticket_roof_on_fire.id,
            "text": "Issue Resolved with phone call",
            "user_id": user_3.id,
        },
    )
    NotesModel.create(
        schema=NotesSchema,
        payload={
            "ticket_id": ticket_dumpster_fire.id,
            "text": "Contacted Tenant -- follow up tomorrow.",
            "user_id": user_3.id,
        },
    )

    EmergencyContactModel.create(
        schema=EmergencyContactSchema,
        payload={
            "name": "Narcotics Anonymous",
            "contact_numbers": [{"number": "503-345-9839"}],
        },
    )

    EmergencyContactModel.create(
        schema=EmergencyContactSchema,
        payload={
            "name": "Washington Co. Crisis Team",
            "description": "Suicide prevention and referrals",
            "contact_numbers": [
                {"number": "503-291-9111", "numtype": "Call"},
                {"number": "503-555-3321", "numtype": "Text"},
            ],
        },
    )

    EmergencyContactModel.create(
        schema=EmergencyContactSchema,
        payload={
            "name": "Child Abuse/Reporting",
            "contact_numbers": [{"number": "503-730-3100"}],
        },
    )

    LeaseModel.create(
        schema=LeaseSchema,
        payload={
            "propertyID": property_test1.id,
            "tenantID": tenant_renty_mcrenter.id,
            "dateTimeStart": Time.yesterday_iso(),
            "dateTimeEnd": Time.one_year_from_now_iso(),
            "occupants": 3,
            "unitNum": "123",
        },
    )
    LeaseModel.create(
        schema=LeaseSchema,
        payload={
            "propertyID": property_meerkat_manor.id,
            "tenantID": tenant_soho_muless.id,
            "dateTimeStart": Time.yesterday_iso(),
            "dateTimeEnd": Time.one_year_from_now_iso(),
            "occupants": 2,
            "unitNum": "418",
        },
    )
    LeaseModel.create(
        schema=LeaseSchema,
        payload={
            "propertyID": property_the_reginald.id,
            "tenantID": tenant_starvin_artist.id,
            "dateTimeStart": Time.yesterday_iso(),
            "dateTimeEnd": Time.one_year_from_now_iso(),
            "occupants": 1,
            "unitNum": "D2",
        },
    )

    print("##########################")
    print("##########################")
    print("    SEED SUCCESSFUL")
    print("##########################")


def user_attributes(fake, role=None, archived=False):
    attrs = {
        "email": fake.unique.email(),
        "password": "1234",
        "firstName": fake.first_name(),
        "lastName": fake.last_name(),
        "phone": fake.phone_number(),
        "archived": archived,
    }
    user_role = {"role": role} if role else {}
    return {**attrs, **user_role}
