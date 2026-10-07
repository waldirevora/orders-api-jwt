from flask import Flask


def create_app():
    """Cria e configura a aplicação Flask."""

    app = Flask(__name__)

    @app.get("/")
    def home():
        """Confirma que a API está em execução."""
        return {"message": "Orders API is running"}

    return app