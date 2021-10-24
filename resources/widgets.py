from flask_restful import Resource
from utils.authorizations import pm_level_required

from models.dashboard import Dashboard


class Widgets(Resource):
    @pm_level_required
    def get(self):
        return Dashboard.json()
