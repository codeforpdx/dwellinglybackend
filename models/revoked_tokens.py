from db import db
from models.base_model import BaseModel


class RevokedTokensModel(BaseModel):
    __tablename__ = 'revoked_tokens'

    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(120))

    def __init__(self, jti):
        self.jti = jti

    @classmethod
    def is_jti_blacklisted(cls, jti):
        return bool(cls.find_by_id(jti))
