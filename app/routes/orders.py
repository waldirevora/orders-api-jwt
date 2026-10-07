from flask import Blueprint

from app.auth import token_required
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