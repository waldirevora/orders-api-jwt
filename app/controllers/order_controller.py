from app.extensions import db
from app.models import Order


def get_user_orders(current_user):
    """Retorna os pedidos pertencentes ao usuário autenticado."""

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


def create_user_order(current_user, description):
    """Cria um pedido associado ao usuário autenticado."""

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