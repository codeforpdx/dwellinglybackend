from models.user import UserModel
from models.tickets import TicketModel
from marshmallow import fields, Schema, validates, ValidationError


class NotesSchema(Schema):
    id = fields.Integer()
    text = fields.Str()
    user_id = fields.Integer(required=True)
    ticket_id = fields.Integer(required=True)

    user = fields.Nested("UserSchema")
    user = fields.Method("showFullName")

    def showFullName(self, obj):
        return "%s %s" % (obj.user.firstName, obj.user.lastName)

    @validates("user_id")
    def validate_existing_user(self, value):
        if not UserModel.query.get(value):
            raise ValidationError(f"{value} is not a valid User ID")

    @validates("ticket_id")
    def validates_existing_ticket(self, value):
        if not TicketModel.query.get(value):
            raise ValidationError(f"{value} is not a valid Ticket ID")
