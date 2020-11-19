from flask_restful import Resource, reqparse
from flask import request

import schemas
from models.emergency_contact import EmergencyContactModel
from models.contact_number import ContactNumberModel
from resources.admin_required import admin_required
from schemas.emergency_contact import EmergencyContactSchema

# Helper function to parse nested ContactNumber dicts from EmergencyContact JSON object into ContactNumberModel
# instances that can be used by SQLAlchemy
def parse_contact_numbers(json_req):
    contact_numbers = []
    for number in json_req.get_json()["contact_numbers"]:
        contact_numbers.append(ContactNumberModel(**number))

    json_req.get_json()["contact_numbers"] = contact_numbers
    return json_req

class EmergencyContacts(Resource):
    # Keeping this here until PUT endpoint has been refactored
    parser = reqparse.RequestParser()
    parser.add_argument('name',type=str,required=True,help="This field cannot be blank")
    parser.add_argument('description',type=str,required=False,help="This field is for the description of the emergency contact")
    parser.add_argument('contact_numbers',action='append',required=True,help="This field cannot be blank")

    def get(self, id=None):
        if id:
            return EmergencyContactModel.find(id).json()
        else:
            return {'emergency_contacts': [e.json() for e in EmergencyContactModel.query.all()]}

    @admin_required
    def post(self):
        EmergencyContactModel.validate_payload(EmergencyContactSchema, request.json)
        validated_request = parse_contact_numbers(request.json)
        EmergencyContactModel.create(validated_request)
        return {'message' : "EmergencyContact created successfully"}, 201

    @admin_required
    def put(self, id):
        parser_for_put = EmergencyContacts.parser.copy()
        parser_for_put.replace_argument('name',required=False)
        parser_for_put.replace_argument('contact_numbers',action='append',required=False)
        data = parser_for_put.parse_args()

        contactEntry = EmergencyContactModel.find_by_id(id)
        if not contactEntry:
            return {'message': 'Emergency contact not found'}, 404

        #variable statements allow for only updated fields to be transmitted
        if(data.name):
            contactEntry.name = data.name
        if('description' in data.keys()):
            contactEntry.description = data.description if data.description else ""

        # TODO: We should/need to create a ContactNumber resource to update this
        if(data.contact_numbers):
            numbersData, numbersError = parse_contact_numbers(request.get_json(force=True))
            if numbersError:
                return {'message': numbersError}, 400
            for number in numbersData:
                contactToModify = ContactNumberModel.find_by_id(number["id"])
                if not contactToModify:
                    contactToModify = ContactNumberModel(
                        emergency_contact_id = id,
                        number = number['number']
                    )
                    contactEntry.contact_numbers.append(contactToModify)
                if "numtype" in number.keys(): contactToModify.numtype = number["numtype"]
                if "extension" in number.keys(): contactToModify.extension = number["extension"]
                contactToModify.save_to_db()

        contactEntry.save_to_db()

        return contactEntry.json()

    @admin_required
    def delete(self, id):
        EmergencyContactModel.delete(id)
        return {'message': 'Emergency contact deleted'}
