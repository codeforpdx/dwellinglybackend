from flask_restful import Resource, reqparse
from models.lease import LeaseModel

class Lease(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name')
    parser.add_argument('unit')
    parser.add_argument('landlordID')
    parser.add_argument('propertyID')
    parser.add_argument('dateStart')
    parser.add_argument('dateEnd')
    parser.add_argument('dateUpdated')

    def get(self, id):
        lease = LeaseModel.find_by_id(id)
        if lease:
            return lease.json()

        return {'Message': 'Lease Not Found'}, 404
    
    def post(self,id):
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