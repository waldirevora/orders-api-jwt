from flask import Blueprint, request
from werkzeug.security import generate_password_hash

from app.extensions import db
from app.models import User


users_bp = Blueprint("users", __name__)


@users_bp.post("/users")
def create_user():
    """Cria um usuário com a senha armazenada como hash."""

    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return {"error": "Username and password are required"}, 400

    existing_user = User.query.filter_by(username=username).first()

    if existing_user:
        return {"error": "Username already exists"}, 409

    user = User(
        username=username,
        password=generate_password_hash(password),
    )

    db.session.add(user)
    db.session.commit()

    return {
        "id": user.id,
        "username": user.username,
    }, 201