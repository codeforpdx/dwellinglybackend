from datetime import datetime, timedelta

from models.tickets import TicketModel
from models.users.property_manager import PropertyManager
from models.property import PropertyModel


class Dashboard:
    @staticmethod
    def json():
        return {
            "opentickets": {
                "new": {
                    "allNew": {
                        "stat": TicketModel.find_count_by_status(TicketModel.NEW),
                        "desc": TicketModel.NEW,
                    },
                    "unseen24Hrs": {
                        "stat": TicketModel.find_count_by_update_status(TicketModel.NEW, 1440),
                        "desc": "Unseen for > 24 hours",
                    },
                },
                "inProgress": {
                    "allInProgress": {
                        "stat": TicketModel.find_count_by_status(TicketModel.IN_PROGRESS),
                        "desc": TicketModel.IN_PROGRESS,
                    },
                    "inProgress1Week": {
                        "stat": TicketModel.find_count_by_update_status(
                            TicketModel.IN_PROGRESS, 10080
                        ),
                        "desc": "In progress for > 1 week",
                    },
                },
            },
            "managers": Dashboard.property_managers(),
        }


    @staticmethod
    def humanize_date(date):
        today = datetime.utcnow().date()
        yesterday = today - timedelta(days=1)
        one_week_ago = today - timedelta(days=7)

        if date == today:
            return "Today"
        elif date == yesterday:
            return "Yesterday"
        elif date >= one_week_ago and date < yesterday:
            return "This Week"

        return date.strftime("%m/%d")

    @staticmethod
    def property_managers():
        managers = []

        for user in PropertyManager.take(3):
            managers.append(
                {
                    "id": user.id,
                    "firstName": user.firstName,
                    "lastName": user.lastName,
                    "date": Dashboard.humanize_date(user.created_at.date()),
                    "propertyName": user.properties[0].name if len(user.properties) > 0 else "Not Assigned"
                }
            )
        return managers
