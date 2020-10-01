from flask_restful import Resource, reqparse
from models.lease import LeaseModel
from models.property import PropertyModel
from datetime import datetime
from flask_jwt_extended import jwt_required

class Lease(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name')
    parser.add_argument('occupants')
    parser.add_argument('landlordID')
    parser.add_argument('propertyID')
    parser.add_argument('tenantID')
    parser.add_argument('dateTimeStart')
    parser.add_argument('dateTimeEnd')
    parser.add_argument('dateUpdated')

    @jwt_required
    def get(self, id):
        lease = LeaseModel.find_by_id(id)
        if lease:
            return lease.json()

        return {'message': 'Lease not found'}, 404

    @jwt_required
    def put(self,id):
        data = Lease.parser.parse_args()
        update = False

        baseLease = LeaseModel.find_by_id(id)
        if not baseLease:
            return {'message': 'Lease not found'}, 404


        if(data.occupants):
            baseLease.occupants = data.occupants
            update = True

        if(data.name):
            baseLease.name = data.name
            update = True

        if(data.landlordID):
            baseLease.landlordID = data.landlordID
            update = True

        if(data.propertyID):
            baseLease.propertyID = data.propertyID
            update = True

        if(data.tenantID):
            baseLease.tenantID = data.tenantID
            update = True

        if(data.dateTimeStart):
            baseLease.dateTimeStart = datetime.strptime(data.dateTimeStart, '%m/%d/%Y %H:%M:%S')
            update = True

        if(data.dateTimeEnd):
            baseLease.dateTimeEnd = datetime.strptime(data.dateTimeEnd, '%m/%d/%Y %H:%M:%S')
            update = True

        if update == False:
            return baseLease.json(), 400
        else:
            baseLease.dateUpdated = datetime.now()

        try:
            baseLease.save_to_db()
        except:
            return {'message': 'An error has occured'}, 500

        return baseLease.json(), 200

    @jwt_required
    def delete(self, id):
        lease = LeaseModel.find_by_id(id)
        if lease:
            lease.delete_from_db()
            return{'message': 'Lease removed from database'}, 200
        else:
            return{'message': 'Lease not found'}, 404

class Leases(Resource):
    @jwt_required
    def get(self):
        return {'Leases': [lease.json() for lease in LeaseModel.query.all()]}

    @jwt_required
    def post(self):
        data = Lease.parser.parse_args()

        #convert strings to DateTime Object
        data.dateTimeStart = datetime.strptime(data.dateTimeStart, '%m/%d/%Y %H:%M:%S')
        data.dateTimeEnd = datetime.strptime(data.dateTimeEnd, '%m/%d/%Y %H:%M:%S')
        data.dateUpdated = datetime.now()

        lease = LeaseModel(**data)

        try:
            lease.save_to_db()
        except:
            return {'message': 'An error has occured'}, 500

        return {'message': 'Lease created successfully'}, 201

