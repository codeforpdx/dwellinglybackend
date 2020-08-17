from flask_restful import Resource, reqparse
import json
from models.tickets import TicketModel
from models.user import UserModel
from flask_jwt_extended import jwt_required 
from datetime import datetime

class Widgets(Resource):
    def get(self):
        newTickets = TicketModel.find_count_by_age_status("New", 1440)
        print(newTickets)
        return {'New': TicketModel.find_count_by_status("New"), 
        'Unseen24': TicketModel.find_count_by_age_status("New", 1440), 
        'InProgress': TicketModel.find_count_by_status("In Progress"), 
        'WeekOld': TicketModel.find_count_by_age_status("In Progress", 10080), 
        'Closed':TicketModel.find_count_by_status("Closed"), 
        'Compliments': 1}, 200
