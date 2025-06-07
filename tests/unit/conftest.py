import pytest
from flask_socketio import SocketIOTestClient

from src.app import create_app, socketio


@pytest.fixture(scope="module")
def test_app():
    """Cria uma instância da aplicação Flask para testes."""
    app = create_app({"TESTING": True})
    return app


@pytest.fixture(scope="module")
def test_client(test_app):
    """Cria um cliente de teste para a aplicação Flask."""
    return test_app.test_client()


@pytest.fixture(scope="module")
def socket_client(test_app):
    """Cria um cliente de teste para o WebSocket."""
    return SocketIOTestClient(test_app, socketio)
