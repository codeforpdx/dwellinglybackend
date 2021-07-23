from flask import current_app, request
from functools import wraps
from typing import Set


def allowed_params(params: Set[str]):
    def decorator(endpoint):
        @wraps(endpoint)
        def verify_fields(*args, **kwargs):
            if not (request.json.keys() <= params):
                return invalid_field_error(params)
            return endpoint(*args, **kwargs)

        return verify_fields

    return decorator


def invalid_field_error(field_set):
    if current_app.env == "production":
        return {"message": "Invalid request field"}, 400
    else:
        raise GatekeeperError(field_set)


class GatekeeperError(Exception):
    def __init__(self, field_set, message="Invalid request field"):
        self.field_set = field_set
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message}: request fields must be one or more of {self.field_set}"
