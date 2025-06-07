from pathlib import Path

from flask import Flask, render_template
from flask_socketio import SocketIO

from src.repository.database import db

BASE_DIR = Path.cwd()
HOST = "http://127.0.0.1:5000"

socketio = SocketIO()


def create_app(config=None):
    """Cria e configura a aplicação Flask dinamicamente."""
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{BASE_DIR}/database/database.db"
    app.config["SECRET_KEY"] = "admin123"

    app.config.update(config or {})

    db.init_app(app)
    socketio.init_app(app)

    @app.route("/")
    def index():
        return render_template("index.html")

    @socketio.on("message")
    def handle_message(msg):
        print(f"Mensagem recebida pelo servidor: {msg}")
        socketio.send(msg)

    return app


def run_app(config=None, debug=False):
    """Executa a aplicação corretamente."""
    app = create_app(config)
    socketio.run(app, debug=debug)


if __name__ == "__main__":
    run_app(debug=True)
