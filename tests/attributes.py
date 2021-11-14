# Attribute methods here should have no 3rd party dependencies.
# Meaning no 3rd party libraries should be imported here so that
# these can be used in the seed file on the remote dev server
# without needing to import additional libraries that are not needed.
# This mostly concerns libraries that would not be used in Production.
from utils.time import Time
from models.tickets import TicketModel


def contact_number_attrs(faker):
    return {
        "number": faker.phone_number(),
        "numtype": faker.random_element(("home", "work", "mobile")),
        "extension": faker.bothify(text="?###"),
    }


def emergency_contact_attrs(faker):
    return {
        "name": faker.name().upper(),
        "description": faker.sentence(nb_words=5),
    }


def property_attrs(faker, archived=False):
    return {
        "name": faker.unique.company(),
        "address": faker.street_address(),
        "city": faker.city(),
        "num_units": faker.random_int(min=1),
        "state": faker.state(),
        "zipcode": faker.postcode(),
        "archived": archived,
    }


def tenant_attrs(faker):
    return {
        "firstName": faker.first_name(),
        "lastName": faker.last_name(),
        "phone": faker.phone_number(),
    }


def lease_attrs(faker, unitNum=None, dateTimeStart=None, dateTimeEnd=None):
    return {
        "unitNum": unitNum or faker.building_number(),
        "dateTimeStart": Time.to_iso(dateTimeStart or faker.date_time_this_decade()),
        "dateTimeEnd": Time.to_iso(
            dateTimeEnd or faker.date_time_this_decade(before_now=False, after_now=True)
        ),
        "occupants": faker.random_number(digits=2),
    }


def ticket_attrs(faker, issue=None, status=None):
    return {
        "issue": issue or faker.sentence(),
        "urgency": faker.random_element(("Low", "Medium", "High")),
        "status": status or faker.random_element(TicketModel.STATUSES),
    }


def note_attrs(faker, text=None):
    return {"text": text or faker.paragraph()}
