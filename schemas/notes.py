from ma import ma
from models.notes import NotesModel
from models.user import UserModel
from utils.time import time_format
from marshmallow import fields, validates, ValidationError

class NotesSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = NotesModel
        include_fk = True
        include_relationships = True
        exclude = ["userinfo"]

    created_at = fields.DateTime(time_format)
    updated_at = fields.DateTime(time_format)

    userinfo = fields.Nested("UserSchema")
    user = fields.Method("showFullName", deserialize = "getUserId")
    def showFullName(self, obj):
        return "%s %s" % (obj.userinfo.firstName, obj.userinfo.lastName)

    def getUserId(self, value):
        return int(value)

    @validates("user")
    def validate_existing_user(self, value):
        if UserModel.find_by_id(value) is None:
            raise ValidationError("No such user")

