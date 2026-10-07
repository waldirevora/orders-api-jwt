from flask import Flask
from app.routes.users import users_bp

from app.extensions import db


def create_app():
    """Cria e configura a aplicação Flask."""

    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///orders.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    app.register_blueprint(users_bp)

    @app.get("/")
    def home():
        """Confirma que a API está em execução."""
        return {"message": "Orders API is running"}

    return app