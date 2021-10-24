
from datetime import datetime, timedelta

from models.tickets import TicketModel
from models.user import UserModel
from models.property import PropertyModel


class Dashboard:
    @staticmethod
    def json():
        users = UserModel.find_recent_role("PROPERTY_MANAGER", 5)
        projectManagers = []

        for user in users:
            date = Dashboard.humanize_date(user.created_at)
            propertyName = Dashboard.property_name(user.id)
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
        }


    @staticmethod
    def humanize_date(date):
        stat = date.strftime("%m/%d")
        today = datetime.utcnow()
        yesterday = today - timedelta(days=1)
        week = today - timedelta(days=7)

        if date.date() == today.date():
            stat = "Today"
        elif date.date() == yesterday.date():
            stat = "Yesterday"
        elif date.date() >= week.date() and date.date() < yesterday.date():
            stat = "This Week"

        return stat

    @staticmethod
    def property_name(user_id):
        # returns the first property to keep things tidy, could add feature later
        property = PropertyModel.find_by_manager(user_id)
        propertyName = "Not Assigned"

        if len(property):
            propertyName = property[0].name

        return propertyName
