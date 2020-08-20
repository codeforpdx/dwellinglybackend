from flask_restful import Resource, reqparse
import json
from models.tickets import TicketModel
from models.user import UserModel
from models.property import PropertyModel
from flask_jwt_extended import jwt_required 
from datetime import datetime

class Widgets(Resource):
    # @jwt_required
   
    def get(self):
        users = UserModel.find_recent_role("property-manager", 5)
        projectManagers = []
        for user in users:
            print(user.widgetJson)
            projectManagers.append(user)

        return { 'opentickets':{
            'title': 'Open Tickets', 
            'stats': [[
                {
                    "stat": TicketModel.find_count_by_status("New"),
                    "desc": 'New',
                },
                {
                    "stat": TicketModel.find_count_by_age_status("New", 1440),
                    "desc": "Unseen for > 24 hours",
                }
            ],
            [
                {
                    "stat": TicketModel.find_count_by_status("In Progress"),
                    "desc": 'In Progress'
                },
                {
                    "stat": TicketModel.find_count_by_age_status("In Progress", 10080),
                    "desc": 'In progress for > 1 week',
                }
            ]]
        },
        'reports':{
            'title': 'Reports',
            'link': '#',
            'stats': [
                [ 
                    {
                        'stat': 0,
                        'desc': 'Compliments',
                        'subtext': 'in the last week'
                    },
                ],
                [
                    {
                        'stat': TicketModel.find_count_by_status("Closed"),
                        'desc': "Closed tickets",
                        'subtext': 'in the last week'
                    }
                ]
            ]
        },
        'managers':{
                'title': 'New Property Managers',
                'link': '#',
                'isDate': True,
                'stats': [
                    [ 
                        {
                            'stat': 'Today',
                            'desc': 'Property Manager Name',
                            'subtext': 'Meerkat Manor'
                        },
                        {
                        'stat': '01/14',
                        'desc': 'Property Manager Name',
                        'subtext': 'Meerkat Manor'
                        },
                        {
                            'stat': '02/04',
                            'desc': 'Property Manager Name',
                            'subtext': 'Meerkat Manor'
                        },
                    ],
                ]
            }
        }, 200
        
        
        
        # {'New': TicketModel.find_count_by_status("New"), 
        # 'Unseen24': TicketModel.find_count_by_age_status("New", 1440), 
        # 'InProgress': TicketModel.find_count_by_status("In Progress"), 
        # 'WeekOld': TicketModel.find_count_by_age_status("In Progress", 10080), 
        # 'Closed':TicketModel.find_count_by_status("Closed"), 
        # 'Compliments': 1}, 200

