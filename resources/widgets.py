from flask_restful import Resource
from models.tickets import TicketModel
from models.user import UserModel
from models.property import PropertyModel
from utils.authorizations import pm_level_required
from datetime import datetime, timedelta


class Widgets(Resource):
    def dateStringConversion(self, date):
        stat = date.strftime("%m/%d")
        today = datetime.utcnow()
        yesterday = today - timedelta(days=1)
        week = today - timedelta(days=1)

        if date.date() == today.date():
            stat = "Today"
        elif date.date() == yesterday.date():
            stat = "Yesterday"
        elif date.date() >= week.date() and date.date() < yesterday.date():
            stat = "This Week"

        return stat

    def returnPropertyName(self, userID):
        # returns the first property to keep things tidy, could add feature later
        property = PropertyModel.find_by_manager(userID)
        propertyName = "Not Assigned"

        if len(property):
            propertyName = property[0].name

        return propertyName

    @pm_level_required
    def get(self):
        users = UserModel.find_recent_role("PROPERTY_MANAGER", 5)
        projectManagers = []

        for user in users:
            date = self.dateStringConversion(user.created_at)
            propertyName = self.returnPropertyName(user.id)
            projectManagers.append(
                {
                    "id": user.id,
                    "firstName": user.firstName,
                    "lastName": user.lastName,
                    "date": date,
                    "propertyName": propertyName,
                }
            )

        return {
            "opentickets": {
                "new": {
                    "allNew": {
                        "stat": TicketModel.find_count_by_status("New"),
                        "desc": "New",
                    },
                    "unseen24Hrs": {
                        "stat": TicketModel.find_count_by_update_status("New", 1440),
                        "desc": "Unseen for > 24 hours",
                    },
                },
                "inProgress": {
                    "allInProgress": {
                        "stat": TicketModel.find_count_by_status("In Progress"),
                        "desc": "In Progress",
                    },
                    "inProgress1Week": {
                        "stat": TicketModel.find_count_by_update_status(
                            "In Progress", 10080
                        ),
                        "desc": "In progress for > 1 week",
                    },
                },
            },
            "managers": projectManagers,
        }, 200
