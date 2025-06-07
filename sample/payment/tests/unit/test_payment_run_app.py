from unittest.mock import patch

import pytest
from flask_socketio import SocketIOTestClient

from sample.payment.src.app import create_app, run_app, socketio


@pytest.fixture(scope="module")
def test_server():
    """Cria uma instância da aplicação Flask para testes."""
    app = create_app({"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"})
    return app


def test_run_app():
    """Testa se `run_app()` executa corretamente e chama `socketio.run()`."""
    config = {"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"}
    with patch("sample.payment.src.app.socketio.run") as mock_socketio_run:
        run_app(config, debug=False)
        mock_socketio_run.assert_called_once()


def test_socket_connection(test_server):
    """Testa conexão e desconexão via WebSocket corretamente."""
    socket_client = SocketIOTestClient(test_server, socketio)
    assert socket_client.is_connected() is True, "Erro ao conectar ao WebSocket"
    socket_client.disconnect()
    assert socket_client.is_connected() is False, "Erro ao desconectar do WebSocket"


def test_run_app_initialization(test_server):
    """Verifica se a aplicação inicia corretamente e responde a requisições."""
    client = test_server.test_client()
    response = client.get("/")
    assert response.status_code in [
        200,
        404,
    ], "A aplicação não inicializou corretamente"
