# Seed file for generating fake data for development.
#
# The seed file is not used within the context of the flask framework
# All models that are explicitly and implicitly used need to be loaded.
# Flake 8 will throw F401 errors in this file. Need to ignore them otherwise
# implicit imports in models will fail to load.
#

import random
from faker import Faker

from db import db
from models.user import UserModel, RoleEnum
from models.users.admin import Admin
from models.users.staff import Staff
from models.users.property_manager import PropertyManager
from models.property import PropertyModel
from models.tenant import TenantModel
from models.tickets import TicketModel
from models.notes import NotesModel
from models.emergency_contact import EmergencyContactModel
from models.contact_number import ContactNumberModel  # noqa: F401
from models.lease import LeaseModel
from schemas import *  # noqa: F403
from tests.attributes import *  # noqa: F403


MIN_HOUSED_TENANTS = 150
MIN_TENANTS = 300
MAX_TENANTS = 500


class Seed:
    def minimal_data(self):
        self.create_admin()

    def data(self):
        print("Seeding the db... This may take a few minutes.")
        self.faker = Faker()
        self.rand = random.Random()

        self.create_admin()

        # Create some admins
        for _ in range(7):
            Admin.create(
                schema=UserSchema,
                payload=self.user_attributes(role=RoleEnum.ADMIN.value),
            )

        # Create some archived admins
        for _ in range(2):
            Admin.create(
                schema=UserSchema,
                payload=self.user_attributes(role=RoleEnum.ADMIN.value, archived=True),
            )

        # Create some pending users
        for _ in range(5):
            self.create_pending_user(payload=self.user_attributes())

        # Create some archived users that were never approved.
        for _ in range(3):
            self.create_pending_user(payload=self.user_attributes(archived=True))

        self.staff = [
            Staff.create(
                schema=UserSchema,
                payload=self.user_attributes(role=RoleEnum.STAFF.value),
            )
            for _ in range(self.rand.randint(30, 50))
        ]

        for _ in range(self.rand.randint(30, 50)):
            Staff.create(
                schema=UserSchema,
                payload=self.user_attributes(role=RoleEnum.STAFF.value, archived=True),
            )

        self.tenants = [
            TenantModel.create(
                schema=TenantSchema,
                payload=self.tenant_attributes(),
            )
            for _ in range(self.rand.randint(MIN_TENANTS, MAX_TENANTS))
        ]

        tenants = self.rand.sample(self.tenants, self.rand.randint(25, 75))
        for tenant in tenants:
            tenant.archived = True
            tenant.save_to_db()

        self.property_managers = [
            self.create_property_manager(
                self.user_attributes(role=RoleEnum.PROPERTY_MANAGER.value)
            )
            for _ in range(self.rand.randint(70, 100))
        ]

        for _ in range(self.rand.randint(30, 50)):
            PropertyManager.create(
                schema=UserSchema,
                payload=self.user_attributes(
                    role=RoleEnum.PROPERTY_MANAGER.value, archived=True
                ),
            )

        self.properties = [
            PropertyModel.create(
                schema=PropertySchema,
                payload=self.property_attributes(),
            )
            for _ in range(self.rand.randint(70, 100))
        ]

        for _ in range(random.randint(0, 15)):
            PropertyModel.create(
                schema=PropertySchema,
                payload=self.property_attributes(archived=True),
            )

        _tenants = self.rand.sample(self.tenants, len(self.tenants))
        _num_leases = self.rand.randint(MIN_HOUSED_TENANTS, MIN_TENANTS)
        for i in range(_num_leases):
            LeaseModel.create(
                schema=LeaseSchema,
                payload={
                    **lease_attrs(self.faker),
                    "propertyID": self.rand.choice(self.properties).id,
                    "tenantID": _tenants[i].id,
                },
            )

        _approved_users = UserModel.query.where(UserModel.type != "user").all()
        self.tickets = [
            TicketModel.create(
                schema=TicketSchema,
                payload={
                    **ticket_attrs(self.faker),
                    "tenant_id": _tenants[self.rand.randint(0, _num_leases)].id,
                    "author_id": self.rand.choice(_approved_users).id,
                },
            )
            for _ in range(self.rand.randint(500, 2000))
        ]

        _tickets = self.rand.sample(self.tickets, len(self.tickets) // 2)
        for ticket in _tickets:
            NotesModel.create(
                schema=NotesSchema,
                payload={
                    **note_attrs(self.faker),
                    "ticket_id": ticket.id,
                    "user_id": self.rand.choice(_approved_users).id,
                },
            )

        for _ in range(self.rand.randint(30, 50)):
            EmergencyContactModel.create(
                schema=EmergencyContactSchema,
                payload={
                    **emergency_contact_attrs(self.faker),
                    "contact_numbers": [
                        contact_number_attrs(self.faker)
                        for _ in range(self.rand.randint(1, 3))
                    ],
                },
            )

        active_admins = len(Admin.query.where(Admin.archived == False).all())
        archived_admins = len(Admin.query.where(Admin.archived == True).all())
        active_staff = len(Staff.query.where(Staff.archived == False).all())
        archived_staff = len(Staff.query.where(Staff.archived == True).all())
        active_pms = len(
            PropertyManager.query.where(PropertyManager.archived == False).all()
        )
        archived_pms = len(
            PropertyManager.query.where(PropertyManager.archived == True).all()
        )
        pending_users = len(
            UserModel.query.where(
                UserModel.archived == False, UserModel.type == "user"
            ).all()
        )
        denied_users = len(
            UserModel.query.where(
                UserModel.archived == True, UserModel.type == "user"
            ).all()
        )

        active_properties = len(
            PropertyModel.query.where(PropertyModel.archived == False).all()
        )
        archived_properties = len(
            PropertyModel.query.where(PropertyModel.archived == True).all()
        )

        active_tenants = len(
            TenantModel.query.where(TenantModel.archived == False).all()
        )
        archived_tenants = len(
            TenantModel.query.where(TenantModel.archived == True).all()
        )

        tickets = len(TicketModel.query.all())

        contacts = len(EmergencyContactModel.query.all())

        print("\n")
        print("#####################################")
        print("#####################################")
        print("          SEED SUCCESSFUL")
        print("#####################################")
        print("\n")
        print(f"{active_admins} Active admins created")
        print(f"{archived_admins} Archived admins created")
        print(f"{active_staff} Active staff created")
        print(f"{archived_staff} Archived staff created")
        print(f"{active_pms} Active property managers created")
        print(f"{archived_pms} Archived property managers created")
        print(f"{pending_users} Pending users created")
        print(f"{denied_users} Denied users created")
        print(f"{active_properties} Active properties created")
        print(f"{archived_properties} Archived properties created")
        print(f"{active_tenants} Active tenants created")
        print(f"{archived_tenants} Archived tenants created")
        print(f"{_num_leases} Leases created")
        print(f"{tickets} Tickets created")
        print(f"{contacts} Emergency Contacts created")
        print("\n")
        print("#####################################")

    def create_admin(self):
        Admin.create(
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

    def user_attributes(self, role=None, archived=False):
        attrs = {
            "email": self.faker.unique.email(),
            "password": "1234",
            "firstName": self.faker.first_name(),
            "lastName": self.faker.last_name(),
            "phone": self.faker.phone_number(),
            "archived": archived,
        }
        user_role = {"role": role} if role else {}
        return {**attrs, **user_role}

    def tenant_attributes(self, archived=False):
        return {
            **tenant_attrs(self.faker),
            "staffIDs": self.staff_ids(),
            "archived": archived,
        }

    def staff_ids(self):
        staffs = self.rand.sample(self.staff, self.rand.randint(0, 3))
        return [staff.id for staff in staffs]

    def property_attributes(self, archived=False):
        return {
            **property_attrs(self.faker, archived),
            "propertyManagerIDs": self.property_manager_ids(),
        }

    def property_manager_ids(self):
        managers = self.rand.sample(self.property_managers, self.rand.randint(1, 5))
        return [manager.id for manager in managers]

    def create_pending_user(self, payload):
        UserModel.create(
            schema=UserRegisterSchema,
            payload=payload,
        )

    def create_property_manager(self, payload):
        payload["role"] = payload.get("role", RoleEnum.PROPERTY_MANAGER.value)
        return PropertyManager.create(
            schema=UserSchema,
            payload=payload,
        )

    def destroy_all(self):
        db.session.execute(
            """
DO
$$
DECLARE
    stmt text;
BEGIN
    SELECT 'TRUNCATE ' || string_agg(format('%I.%I', schemaname, tablename), ',')
        INTO stmt
    FROM pg_tables
    WHERE schemaname in ('public');

    EXECUTE stmt;
END;
$$
            """
        )
