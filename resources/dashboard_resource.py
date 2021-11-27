from flask_restful import Resource
from utils.authorizations import admin_required

from models.dashboard import Dashboard


class DashboardResource(Resource):
    @admin_required
    def get(self):
        return Dashboard.json()
