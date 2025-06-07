import pytest


@pytest.mark.index_route
class TestIndexRoute:
    """Testes da rota principal da aplicação."""

    def test_index_page(self, test_client):
        """Testa se a página inicial é carregada corretamente."""
        response = test_client.get("/")
        assert response.status_code == 200
        assert b"Chat em Tempo Real" in response.data


@pytest.mark.web_socket
class TestWebSocket:
    """Testes para a conexão e envio de mensagens via WebSocket."""

    def test_websocket_connection(self, socket_client):
        """Testa se o WebSocket conecta corretamente."""
        assert socket_client.is_connected() is True
        socket_client.disconnect()
        assert socket_client.is_connected() is False

    def test_websocket_message(self, socket_client):
        """Testa envio e recebimento de mensagens via WebSocket."""
        socket_client.connect()
        assert socket_client.is_connected() is True

        socket_client.emit("message", "Testando mensagem")
        received = socket_client.get_received()

        assert len(received) > 0
        assert isinstance(
            received[0], dict
        ), "Erro: Estrutura inesperada no evento recebido"
        assert (
            "args" in received[0]
        ), "Erro: Chave `args` não encontrada no evento recebido"

        assert received[0]["args"] == "Testando mensagem"
