from datetime import datetime, timezone

from app.extensions import db


class Order(db.Model):
    """Representa um pedido pertencente a um usuário."""

    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255), nullable=False)
    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
    )