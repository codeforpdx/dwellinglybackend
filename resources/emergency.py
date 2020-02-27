from flask_restful import Resource, reqparse
from flask import request
from models.emergency import EmergencyModel

class EmergencyNumbers(Resource):

    def get(self,id):
        item = next(filter(lambda x: x["id"] == id, emergencyList), None)
        return {"Emergency Number": item}, 200 if item else 404

        #  "id": "00000001",
        # "name": "Test Number 1",
        # "type": "user",
        # "userid": "user1",
        # "number": "555-55-1234"
    def patch(self,id):
        item = next(filter(lambda x: x["id"] == id, emergencyList), None)

        parser = reqparse.RequestParser()
        parser.add_argument('name', help="need a name")
        parser.add_argument('type', help="need type")
        parser.add_argument('userid', help="need userid")
        parser.add_argument('propertyid', help="need propertyid")
        parser.add_argument('number', help="need number")

        request_data = parser.parse_args()

        if item:
            item.update(request_data)
        return {"Emergency Number": item}, 200

    def delete(self, id):
        global emergencyList
        emergencyList = next(filter(lambda x: x["id"] != id, emergencyList), None)
        return {"message": "Emergency Number deleted"}


# multiple propert resources
class Emergency(Resource):
    def get(self):
        return {"Emergency Numbers": emergencyList}, 200 if emergencyList else 404

    def post(self):
        id = "00000000" + str(len(userList)) 
        request_data = request.get_json()

        #  "id": "00000001",
        # "name": "Test Number 1",
        # "type": "user",
        # "userid": "user1",
        # "number": "555-55-1234"

        new_emergency= {
          "id":id,
          "name": request_data["name"],
          "type": request_data["type"],
          "userid": request_data["userid"],
          "propertyid": request_data["propertyid"],
          "number": request_data["number"]
          }
        emergencyList.append(new_emergency)

        return new_emergency, 201

