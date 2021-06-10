from ma import ma
from models.user import UserModel
from models.tickets import TicketModel
from models.notes import NotesModel
from utils.time import time_format
from marshmallow import fields, validates, ValidationError, post_load, EXCLUDE


class NotesSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = NotesModel
        unknown = EXCLUDE

    id = fields.Integer()
    text = fields.Str()
    user_id = fields.Integer(required=True)
    ticket_id = fields.Integer(required=True)

    created_at = fields.DateTime(time_format)
    updated_at = fields.DateTime(time_format)

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

    @post_load
    def make_notes(self, data, **kwargs):
        return NotesModel(**data)
