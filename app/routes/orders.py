from flask import Blueprint, request

from app.auth import token_required
from app.controllers.order_controller import (
    create_user_order,
    get_user_orders,
)


orders_bp = Blueprint("orders", __name__)


@orders_bp.get("/orders")
@token_required
def list_orders(current_user):
    """Recebe a requisição para listar pedidos."""

    return get_user_orders(current_user)


@orders_bp.post("/orders")
@token_required
def create_order(current_user):
    """Recebe a requisição para criar um pedido."""

    data = request.get_json(silent=True) or {}

    return create_user_order(
        current_user,
        data.get("description"),
    )