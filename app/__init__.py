import os

from dotenv import load_dotenv
from flask import Flask

from app.extensions import db
from app.routes.auth import auth_bp
from app.routes.orders import orders_bp
from app.routes.users import users_bp


def create_app(test_config=None):
    """Cria e configura a aplicação Flask."""

    load_dotenv()

    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///orders.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")

    if test_config:
        app.config.update(test_config)

    if not app.config["JWT_SECRET_KEY"]:
        raise RuntimeError("JWT_SECRET_KEY is not configured")

    db.init_app(app)

    app.register_blueprint(users_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(orders_bp)

    @app.get("/")
    def home():
        """Confirma que a API está em execução."""
        return {"message": "Orders API is running"}

    return app