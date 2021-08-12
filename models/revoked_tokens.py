from db import db
from models.base_model import BaseModel


class RevokedTokensModel(BaseModel):
    __tablename__ = "revoked_tokens"

    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False)

    @classmethod
    def is_jti_revoked(cls, jti):
        token = cls.query.filter_by(jti=jti).scalar()
        return token is not None
