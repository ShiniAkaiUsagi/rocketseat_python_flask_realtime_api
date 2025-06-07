from datetime import datetime, timedelta
from pathlib import Path

from flask import Flask, jsonify, render_template, request, send_file
from flask_socketio import SocketIO

from sample.payment.src.db_models.payment import Payment
from sample.payment.src.payments.pix import Pix
from sample.payment.src.repository.database import db

BASE_DIR = Path.cwd() / "sample" / "payment"
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

    @app.route("/payments/pix", methods=["POST"])
    def create_payment_pix():
        data = request.get_json()
        if "value" not in data:
            return jsonify({"message": "Invalid value"}), 400
        expiration_date = datetime.now() + timedelta(minutes=30)
        pix_object = Pix()
        data_payment_pix = pix_object.create_payment()

        new_payment = Payment(
            value=data["value"],
            expiration_date=expiration_date,
            bank_payment_id=str(data_payment_pix["bank_payment_id"]),
            qr_code=data_payment_pix["qr_code_path"],
        )

        db.session.add(new_payment)
        db.session.commit()

        return jsonify(
            {
                "message": "The payment has been created.",
                "payment": new_payment.to_dict(),
            }
        )

    @app.route("/payments/pix/qr_code/<file_name>", methods=["GET"])
    def get_image(file_name):
        file_path = BASE_DIR / "src" / "static" / "img" / f"{file_name}"
        return send_file(file_path, mimetype="image/png")

    @app.route("/payments/pix/confirmation", methods=["POST"])
    def pix_confirmation():
        data = request.get_json()

        if "bank_payment_id" not in data or "value" not in data:
            return jsonify({"message": "Invalid payment data."}), 400

        payment = Payment.query.filter_by(
            bank_payment_id=data.get("bank_payment_id")
        ).first()

        if not payment or payment.paid:
            return jsonify({"message": "Payment not found."}), 404

        if data.get("value") != payment.value:
            return jsonify({"message": "Invalid payment data."}), 400

        payment.paid = True
        db.session.commit()
        socketio.emit(f"payment-confirmed-{payment.id}")
        return jsonify({"message": "The payment has been confirmed."})

    @app.route("/payments/pix/<int:payment_id>", methods=["GET"])
    def payment_pix_page(payment_id):
        payment = Payment.query.get(payment_id)

        if not payment:
            return render_template("404.html")

        if payment.paid:
            return render_template(
                "confirmed_payment.html",
                payment_id=payment.id,
                value=payment.value,
                qr_code=payment.qr_code,
            )

        return render_template(
            "payment.html",
            payment_id=payment.id,
            value=payment.value,
            host=HOST,
            qr_code=payment.qr_code,
            expiration_date=payment.expiration_date,
        )

    # WebSockets
    @socketio.on("connect")
    def handle_connect():
        print("Client connected to the server.")

    @socketio.on("disconnect")
    def handle_disconnect():
        print("Client has disconnected from the server.")

    return app


def run_app(config=None, debug=False):
    """Executa a aplicação corretamente."""
    app = create_app(config)
    socketio.run(app, debug=debug)


if __name__ == "__main__":
    run_app(debug=True)
