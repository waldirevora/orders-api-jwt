import pytest

from app import create_app
from app.extensions import db


@pytest.fixture
def app():
    """Cria uma aplicação isolada para cada teste."""

    app = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "JWT_SECRET_KEY": "test-secret-key-with-at-least-32-bytes",
        }
    )

    with app.app_context():
        db.create_all()

        yield app

        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Disponibiliza o cliente HTTP de testes do Flask."""

    return app.test_client()