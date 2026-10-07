from flask import Blueprint, request

from app.auth import token_required
from app.extensions import db
from app.models import Order


orders_bp = Blueprint("orders", __name__)


@orders_bp.get("/orders")
@token_required
def list_orders(current_user):
    """Lista apenas os pedidos do usuário autenticado."""

    orders = Order.query.filter_by(user_id=current_user.id).all()

    return {
        "orders": [
            {
                "id": order.id,
                "description": order.description,
                "created_at": order.created_at.isoformat(),
            }
            for order in orders
        ]
    }, 200


@orders_bp.post("/orders")
@token_required
def create_order(current_user):
    """Cria um pedido para o usuário autenticado."""

    data = request.get_json(silent=True) or {}
    description = data.get("description")

    if not isinstance(description, str) or not description.strip():
        return {"error": "Description is required"}, 400

    order = Order(
        description=description.strip(),
        user_id=current_user.id,
    )

    db.session.add(order)
    db.session.commit()

    return {
        "id": order.id,
        "description": order.description,
        "created_at": order.created_at.isoformat(),
    }, 201