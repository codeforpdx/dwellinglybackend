from db import db
from models.base_model import BaseModel


class RevokedTokensModel(BaseModel):
    __tablename__ = "revoked_tokens"

    id = db.Column(db.String(36), primary_key=True)
    jti = db.Column(db.String(120), nullable=False)

    @classmethod
    def is_jti_blacklisted(cls, jti):
        return bool(cls.query.get(jti))
