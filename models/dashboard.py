from models.tickets import TicketModel
from models.users.property_manager import PropertyManager
from models.tenant import TenantModel
from models.users.staff import Staff
from models.user import UserModel
from utils.time import Date


class Dashboard:
    @staticmethod
    def json():
        return {
            "tickets": {
                "new": {
                    "total_count": TicketModel.new().count(),
                    "latent_count": TicketModel.new().updated_within(days=1).count(),
                },
                "in_progress": {
                    "total_count": TicketModel.in_progress().count(),
                    "latent_count": TicketModel.in_progress()
                    .updated_within(days=7)
                    .count(),
                },
            },
            "managers": [Dashboard._manager_json(m) for m in PropertyManager.take(3)],
            "pending_users": UserModel.query.active().pending().json(),
            "staff": Staff.query.json(),
            "tenants": TenantModel.query.active()
            .unassigned_staff()
            .order_by(TenantModel.updated_at.asc())
            .json(),
        }

    @staticmethod
    def _manager_json(manager):
        return {
            "id": manager.id,
            "first_name": manager.firstName,
            "last_name": manager.lastName,
            "date": Dashboard._humanize_date(manager.created_at.date()),
            "property_name": manager.properties[0].name
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
