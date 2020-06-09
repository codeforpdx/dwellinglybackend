from flask_restful import Resource, reqparse
from flask import request
from models.emergency_contact import EmergencyContactModel
from models.contact_number import ContactNumberModel
from resources.admin_required import admin_required

# Helper function: Extract contact number info from an array of JSON objects
# Return a tuple with the parsed data and any error messages
def parseContactNumbersFromJson(json_data):
    parsedData = []
    error = None
    json_data = request.get_json(force=True)
    for number in json_data["contact_numbers"]:
        if not 'number' in number.keys(): 
            error = "One of the contact_numbers for the emergency contact is missing a number"
            break
        newNumber = { "number": number['number'], "id": "unavailable" }
        if 'id' in number.keys(): newNumber['id'] = number['id']
        if 'numtype' in number.keys(): newNumber['numtype'] = number['numtype']
        if 'extension' in number.keys(): newNumber['extension'] = number['extension']
        parsedData.append(newNumber)
    return parsedData, error

class EmergencyContacts(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',type=str,required=True,help="This field cannot be blank.")
    parser.add_argument('description',type=str,required=False,help="This field is for the description of the emergency contact.")
    parser.add_argument('contact_numbers',action='append',required=True,help="This field cannot be blank.")

    def get(self, id=None):
        # GET /emergencynumbers
        if not id:
            return {'emergency_contacts': [e.json() for e in EmergencyContactModel.query.all()]}

        # GET /emergencynumbers/<id>
        emergencyEntry = EmergencyContactModel.find_by_id(id)
        if not emergencyEntry:
            return {'message': 'Emergency Contact not found'}, 404
        return emergencyEntry.json()

    @admin_required
    def post(self):
        data = EmergencyContacts.parser.parse_args()
        if EmergencyContactModel.find_by_name(data["name"]):
            return {'message': 'An emergency contact with this name already exists'}, 401

        # In the JSON body, contact_numbers is expected to be an array of dictionaries
        # But, reqparser is not able to extract nested JSON data (see https://github.com/flask-restful/flask-restful/issues/517)
        numbersData, numbersError = parseContactNumbersFromJson(request.get_json(force=True))
        if numbersError:
            return {'message': numbersError}, 401
        data["contact_numbers"] = numbersData

        contactEntry = EmergencyContactModel(**data)
        try:
            EmergencyContactModel.save_to_db(contactEntry)
        except:
            return {"Message": "An Internal Error has Occured. Unable to insert emergency contact"}, 500

        return contactEntry.json(), 201

    @admin_required
    def put(self, id):
        parser_for_put = EmergencyContacts.parser.copy()
        parser_for_put.replace_argument('name',required=False)
        parser_for_put.replace_argument('contact_numbers',action='append',required=False)
        data = parser_for_put.parse_args()

        contactEntry = EmergencyContactModel.find_by_id(id)
        if not contactEntry:
            return {'message': 'Emergency Contact not found.'}, 404

        #variable statements allow for only updated fields to be transmitted 
        if(data.name):
            contactEntry.name = data.name
        if('description' in data.keys()):
            contactEntry.description = data.description if data.description else ""
        if(data.contact_numbers):
            numbersData, numbersError = parseContactNumbersFromJson(request.get_json(force=True))
            if numbersError:
                return {'message': numbersError}, 401
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
        
        try:
            contactEntry.save_to_db()
        except:
            return {"message": "An error has occured updating the emergency contact"}, 500

        return contactEntry.json()

    @admin_required
    def delete(self, id):
        contact = EmergencyContactModel.find_by_id(id)
        if not contact:
            return {'message': 'Emergency Contact not found.'}, 404

        contact.delete_from_db()
        return {'message': 'Emergency Contact deleted.'}
