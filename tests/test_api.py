import jwt


def create_user(client, username):
    """Cria um usuário utilizado pelos testes."""

    return client.post(
        "/users",
        json={
            "username": username,
            "password": "123456",
        },
    )


def login(client, username):
    """Autentica um usuário e retorna seu token."""

    response = client.post(
        "/login",
        json={
            "username": username,
            "password": "123456",
        },
    )

    return response.get_json()["token"]


def test_login_returns_valid_jwt(client, app):
    """Confirma que o login retorna JWT com ID e username."""

    create_user(client, "waldir")

    token = login(client, "waldir")

    payload = jwt.decode(
        token,
        app.config["JWT_SECRET_KEY"],
        algorithms=["HS256"],
    )

    assert payload["user_id"] == 1
    assert payload["username"] == "waldir"


def test_orders_requires_authentication(client):
    """Impede acesso aos pedidos sem JWT."""

    response = client.get("/orders")

    assert response.status_code == 401


def test_user_can_only_list_own_orders(client):
    """Garante isolamento dos pedidos entre usuários."""

    create_user(client, "waldir")
    create_user(client, "user2")

    token1 = login(client, "waldir")
    token2 = login(client, "user2")

    client.post(
        "/orders",
        json={"description": "Pedido Waldir"},
        headers={"Authorization": f"Bearer {token1}"},
    )

    response = client.get(
        "/orders",
        headers={"Authorization": f"Bearer {token2}"},
    )

    data = response.get_json()

    assert response.status_code == 200
    assert data["orders"] == []

def test_authenticated_user_can_create_order(client):
    """Confirma que um usuário autenticado pode criar um pedido."""

    create_user(client, "waldir")
    token = login(client, "waldir")

    response = client.post(
        "/orders",
        json={"description": "Novo pedido"},
        headers={"Authorization": f"Bearer {token}"},
    )

    data = response.get_json()

    assert response.status_code == 201
    assert data["description"] == "Novo pedido"
    assert data["id"] == 1
    