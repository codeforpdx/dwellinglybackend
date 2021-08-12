from flask import request
from flask_restful import Resource
from utils.gatekeeper import allowed_params


class DummyResource(Resource):
    dummy_params = set()

    @allowed_params(dummy_params)
    def put(self):
        return request.json
