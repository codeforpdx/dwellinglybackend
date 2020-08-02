from flask_restful import Resource, reqparse
from models.lease import LeaseModel
from models.property import PropertyModel
from datetime import datetime

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

    def get(self, id):
        lease = LeaseModel.find_by_id(id)
        if lease:
            return lease.json()

        return {'Message': 'Lease Not Found'}, 404
    
    def put(self,id):
        data = Lease.parser.parse_args()

        if LeaseModel.find_by_id(id):
            return{'Message': 'Lease already exists'}, 400
        
        lease = LeaseModel(id)
        try:
            lease.save_to_db()
        except:
            return {'Message': 'An Error Has Occured'}, 500

        return lease.json(), 201

    def delete(self, id):
        lease = LeaseModel.find_by_id(id)
        if lease:
            lease.delete_from_db()

        return{'Message': 'Lease Removed from Database'}

class Leases(Resource):
    def get(self):
        return {'Leases': [lease.json() for lease in LeaseModel.query.all()]}

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
            return {'Message': 'An Error Has Occured'}, 500

        return 201