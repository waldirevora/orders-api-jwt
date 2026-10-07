from datetime import datetime, timedelta, timezone

import jwt
from flask import Blueprint, current_app, request
from werkzeug.security import check_password_hash

from app.models import User


auth_bp = Blueprint("auth", __name__)


@auth_bp.post("/login")
def login():
    """Autentica o usuário e retorna um token JWT."""

    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return {"error": "Username and password are required"}, 400

    user = User.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.password, password):
        return {"error": "Invalid username or password"}, 401

    payload = {
        "user_id": user.id,
        "username": user.username,
        "exp": datetime.now(timezone.utc) + timedelta(hours=1),
    }

    token = jwt.encode(
        payload,
        current_app.config["JWT_SECRET_KEY"],
        algorithm="HS256",
    )

    return {"token": token}, 200