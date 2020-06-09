from flask_restful import Resource, reqparse
from flask import request
from models.emergency_contact import EmergencyContactModel

class EmergencyContacts(Resource):

    def get(self, id=None):
        # GET /emergencynumbers
        if not id:
            return {'emergency_contacts': [e.json() for e in EmergencyContactModel.query.all()]}

        emergencyEntry = EmergencyContactModel.find_by_id(id)
        
        if not emergencyEntry:
            return {'message': 'Emergency Contact not found'}, 404
        return emergencyEntry.json()

    # def patch(self,id):
    #     item = next(filter(lambda x: x["id"] == id, emergencyList), None)

    #     parser = reqparse.RequestParser()
    #     parser.add_argument('name', help="need a name")
    #     parser.add_argument('type', help="need type")
    #     parser.add_argument('userid', help="need userid")
    #     parser.add_argument('propertyid', help="need propertyid")
    #     parser.add_argument('number', help="need number")

    #     request_data = parser.parse_args()

    #     if item:
    #         item.update(request_data)
    #     return {"Emergency Number": item}, 200

    # def delete(self, id):
    #     global emergencyList
    #     emergencyList = next(filter(lambda x: x["id"] != id, emergencyList), None)
    #     return {"message": "Emergency Number deleted"}

    # def post(self):
    #     id = "00000000" + str(len(userList)) 
    #     request_data = request.get_json()

    #     #  "id": "00000001",
    #     # "name": "Test Number 1",
    #     # "type": "user",
    #     # "userid": "user1",
    #     # "number": "555-55-1234"

    #     new_emergency= {
    #       "id":id,
    #       "name": request_data["name"],
    #       "type": request_data["type"],
    #       "number": request_data["number"]
    #       }
    #     emergencyList.append(new_emergency)

    #     return new_emergency, 201

