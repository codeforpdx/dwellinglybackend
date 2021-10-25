from models.tickets import TicketModel
from models.users.property_manager import PropertyManager
from utils.time import Date


class Dashboard:
    @staticmethod
    def json():
        return {
            "opentickets": {
                "new": {
                    "allNew": {
                        "stat": TicketModel.new().count(),
                    },
                    "unseen24Hrs": {
                        "stat": TicketModel.new().updated_within(days=1).count(),
                    },
                },
                "inProgress": {
                    "allInProgress": {
                        "stat": TicketModel.in_progress().count(),
                    },
                    "inProgress1Week": {
                        "stat": TicketModel.in_progress()
                        .updated_within(days=7)
                        .count(),
                    },
                },
            },
            "managers": [Dashboard._manager_json(m) for m in PropertyManager.take(3)],
        }

    # Below is what I would like to use instead of the above json^^^
    @staticmethod
    def proposed_json():
        return {
            "new_count": TicketModel.new().count(),
            "recent_new_count": TicketModel.new().updated_within(days=1).count(),
            "in_progress_count": TicketModel.in_progress().count(),
            "recent_in_progress_count": TicketModel.in_progress()
            .updated_within(days=7)
            .count(),
            "managers": [Dashboard._manager_json(m) for m in PropertyManager.take(3)],
        }

    @staticmethod
    def _manager_json(manager):
        return {
            "id": manager.id,
            "firstName": manager.firstName,
            "lastName": manager.lastName,
            "date": Dashboard._humanize_date(manager.created_at.date()),
            "propertyName": manager.properties[0].name
            if len(manager.properties) > 0
            else "Not Assigned",
        }

    @staticmethod
    def _humanize_date(date):
        if date == Date.today():
            return "Today"
        elif date == Date.days_ago(1):
            return "Yesterday"
        elif date >= Date.weeks_ago(1):
            return "This Week"

        return date.strftime("%m/%d")
