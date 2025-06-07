import uuid
from datetime import datetime, timedelta
from pathlib import Path

import pytest
import qrcode

from sample.payment.src.app import create_app
from sample.payment.src.db_models.payment import Payment
from sample.payment.src.repository.database import db

QR_CODE_IMG_DIR = Path.cwd() / "sample" / "payment" / "src" / "static" / "img"


@pytest.fixture(scope="session")
def test_app():
    """Cria uma instância de aplicação Flask para testes."""
    config = {"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"}
    app = create_app(config)  # 🔹 Criamos a aplicação sem iniciar o servidor
    return app


@pytest.fixture(scope="function")
def client(test_app):
    """Cria um cliente de teste Flask dentro de um contexto válido."""
    with test_app.app_context():
        with test_app.test_client() as client:
            db.create_all()
            yield client
            db.drop_all()


@pytest.fixture(scope="function")
def payment_fixture(client):
    """Cria um pagamento real no banco e retorna o objeto atualizado."""
    with client.application.app_context():
        bank_payment_id = str(uuid.uuid4())
        expiration_date = datetime.now() + timedelta(minutes=30)

        hash_payment = f"hash_payment_{bank_payment_id}"
        img = qrcode.make(hash_payment)
        img_file_name = f"qr_code_payment_{bank_payment_id}.png"
        img_path = QR_CODE_IMG_DIR / img_file_name
        img.save(img_path)

        payment = Payment(
            value=100,
            expiration_date=expiration_date,
            bank_payment_id=bank_payment_id,
            qr_code=img_file_name,
        )
        db.session.add(payment)
        db.session.commit()

        return Payment.query.filter_by(bank_payment_id=bank_payment_id).first()
