from models.user import UserModel
from models.tickets import TicketModel
from utils.time import time_format
from marshmallow import fields, Schema, validates, ValidationError


class NotesSchema(Schema):
    id = fields.Integer()
    text = fields.Str()
    userid = fields.Integer(required=True)
    ticketid = fields.Integer(required=True)

    created_at = fields.DateTime(time_format)
    updated_at = fields.DateTime(time_format)

    user = fields.Nested("UserSchema")
    user = fields.Method("showFullName")

    def showFullName(self, obj):
        return "%s %s" % (obj.user.firstName, obj.user.lastName)

    @validates("userid")
    def validate_existing_user(self, value):
        if UserModel.find_by_id(value) is None:
            raise ValidationError("No such user")

    @validates("ticketid")
    def validates_existing_ticket(self, value):
        if TicketModel.find_by_id(value) is None:
            raise ValidationError("No ticket with id: %s exists" % (value))
