from flask_restful import Resource, reqparse
import json
from models.tickets import TicketModel
from models.user import UserModel
from models.property import PropertyModel
from flask_jwt_extended import jwt_required 
from datetime import datetime, timedelta

class Widgets(Resource):

    def dateStringConversion(self, date):
        stat = date.strftime('%m/%d')
        today = datetime.now()
        yesterday = today - timedelta(days = 1)
        week = today - timedelta(days = 1)

        if date.date() == today.date():
            stat = "Today"
        elif date.date() == yesterday.date():
            stat = "Yesterday"
        elif date.date() >= week.date() & date.date() < yesterday.date():
            stat = "This Week"

        return stat

    def returnPropertyName(self, userID):
        #returns the first property to keep things tidy, could add feature later
        property = PropertyModel.find_by_manager(userID)
        propertyName = "Not Assigned"

        if property[0]: 
            propertyName = property[0].name

        return propertyName

    # @jwt_required
    def get(self):
        users = UserModel.find_recent_role("property-manager", 5)
        projectManagers = []

        nullPropertyManager  = { 'id': " ",
            'stat': " ",
            'desc': "No new users",
            'subtext': " "
            }

        for user in users:
            date = self.dateStringConversion(user.created)
            propertyName = self.returnPropertyName(user.id)           
            projectManagers.append(user.widgetJson(propertyName, date))

        if len(projectManagers) == 0:
            print("no managers")
            projectManagers.append(nullPropertyManager)

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
                        'subtext': 'in the last week!'
                    }
                ]
            ]
        },
        'managers':{
                'title': 'New Property Managers',
                'link': '#',
                'isDate': True,
                'stats': [projectManagers]
            }
        }, 200
