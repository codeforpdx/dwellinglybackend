from flask_restful import Resource, reqparse
from flask import request

from models.emergency_contact import EmergencyContactModel
from models.contact_number import ContactNumberModel
from utils.authorizations import admin_required
from schemas.emergency_contact import EmergencyContactSchema


# Not sure if this is necessary anymore
def parse_contact_numbers(req):
    contact_numbers = []
    for number in req["contact_numbers"]:
        contact_numbers.append(ContactNumberModel(**number))

    req["contact_numbers"] = contact_numbers
    return req


def parseContactNumbersFromJson(json_data):
    parsedData = []
    error = None
    json_data = request.get_json(force=True)
    for number in json_data["contact_numbers"]:
        if "number" not in number.keys():
            error = "A contact number for the emergency contact is missing a number"
            break
        newNumber = {"number": number["number"], "id": "unavailable"}
        if "id" in number.keys():
            newNumber["id"] = number["id"]
        if "numtype" in number.keys():
            newNumber["numtype"] = number["numtype"]
        if "extension" in number.keys():
            newNumber["extension"] = number["extension"]
        parsedData.append(newNumber)
    return parsedData, error


class EmergencyContacts(Resource):
    def get(self):
        return {"emergency_contacts": EmergencyContactModel.query.json()}

    @admin_required
    def post(self):
        return (
            EmergencyContactModel.create(
                schema=EmergencyContactSchema, payload=request.json
            ).json(),
            201,
        )


class EmergencyContact(Resource):
    def get(self, id):
        return EmergencyContactModel.find(id).json()

    # Keeping this here until PUT endpoint has been refactored
    parser = reqparse.RequestParser()
    parser.add_argument(
        "name", type=str, required=True, help="This field cannot be blank"
    )
    parser.add_argument(
        "description",
        type=str,
        required=False,
        help="This field is for the description of the emergency contact",
    )
    parser.add_argument(
        "contact_numbers",
        action="append",
        required=True,
        help="This field cannot be blank",
    )

    @admin_required
    def put(self, id):
        parser_for_put = EmergencyContacts.parser.copy()
        parser_for_put.replace_argument("name", required=False)
        parser_for_put.replace_argument(
            "contact_numbers", action="append", required=False
        )
        data = parser_for_put.parse_args()

        contactEntry = EmergencyContactModel.find(id)

        # variable statements allow for only updated fields to be transmitted
        if data.name:
            contactEntry.name = data.name
        if "description" in data.keys():
            contactEntry.description = data.description if data.description else ""

        # TODO: We should/need to create a ContactNumber resource to update this
        if data.contact_numbers:
            numbersData, numbersError = parseContactNumbersFromJson(
                request.get_json(force=True)
            )
            if numbersError:
                return {"message": numbersError}, 400
            for number in numbersData:
                contactToModify = ContactNumberModel.find(number["id"])
                if not contactToModify:
                    contactToModify = ContactNumberModel(
                        emergency_contact_id=id, number=number["number"]
                    )
                    contactEntry.contact_numbers.append(contactToModify)
                if "numtype" in number.keys():
                    contactToModify.numtype = number["numtype"]
                if "extension" in number.keys():
                    contactToModify.extension = number["extension"]
                contactToModify.save_to_db()

        contactEntry.save_to_db()

        return contactEntry.json()

    @admin_required
    def delete(self, id):
        EmergencyContactModel.delete(id)
        return {"message": "Emergency contact deleted"}
