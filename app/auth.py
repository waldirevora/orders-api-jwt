from functools import wraps

import jwt
from flask import current_app, request

from app.extensions import db
from app.models import User


def token_required(function):
    """Valida o JWT e identifica o usuário autenticado."""

    @wraps(function)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")

        if not auth_header.startswith("Bearer "):
            return {"error": "Token is required"}, 401

        token = auth_header.replace("Bearer ", "", 1)

        try:
            payload = jwt.decode(
                token,
                current_app.config["JWT_SECRET_KEY"],
                algorithms=["HS256"],
            )
        except jwt.ExpiredSignatureError:
            return {"error": "Token has expired"}, 401
        except jwt.InvalidTokenError:
            return {"error": "Invalid token"}, 401

        user = db.session.get(User, payload.get("user_id"))

        if not user:
            return {"error": "User not found"}, 401

        return function(user, *args, **kwargs)

    return decorated