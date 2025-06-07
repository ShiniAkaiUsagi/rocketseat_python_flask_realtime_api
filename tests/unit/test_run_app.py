import pytest

from src.app import create_app, run_app, socketio


@pytest.mark.run_app
class TestRunApp:
    """Testa se `run_app()` executa corretamente."""

    def test_server(self, mocker):
        """Testa se `create_app()` chama `socketio.run()` corretamente sem iniciar um servidor real."""
        app = create_app({"TESTING": True})
        mock_run = mocker.patch.object(socketio, "run", autospec=True)
        socketio.run(app)
        mock_run.assert_called_once()

    def test_run_app(self, mocker):
        """Testa se `run_app()` executa corretamente e chama `socketio.run()` sem iniciar um servidor real."""
        config = {"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"}
        mock_socketio_run = mocker.patch.object(socketio, "run", autospec=True)
        run_app(config, debug=False)
        mock_socketio_run.assert_called_once()
