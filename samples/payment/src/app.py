from datetime import datetime, timedelta
from pathlib import Path

from flask import Flask, jsonify, render_template, request, send_file
from flask_socketio import SocketIO

from samples.payment.src.db_models.payment import Payment
from samples.payment.src.payments.pix import Pix
from samples.payment.src.repository.database import db

BASE_DIR = Path.cwd() / "samples" / "payment"
HOST = "http://127.0.0.1:5000"


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{BASE_DIR}/database/database.db"
app.config["SECRET_KEY"] = "admin123"


db.init_app(app)
socketio = SocketIO(app)


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
        {"message": "The payment has been created.", "payment": new_payment.to_dict()}
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


# websockets
@socketio.on("connect")
def handle_connect():
    print("client connected to the Server.")


def run_app(debug=False):
    socketio.run(app, debug=debug)


if __name__ == "__main__":
    run_app(debug=True)
