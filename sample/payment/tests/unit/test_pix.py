import pytest

from sample.payment.src.db_models.payment import Payment
from sample.payment.src.repository.database import db


@pytest.mark.create_payment
class TestCreatePaymentPix:
    """Testes para criação de pagamento via Pix."""

    def test_create_payment_pix(self, client):
        response = client.post("/payments/pix", json={"value": 100})
        assert response.status_code == 200
        assert "payment" in response.json

    def test_create_payment_pix_invalid(self, client):
        response = client.post("/payments/pix", json={})
        assert response.status_code == 400
        assert response.json["message"] == "Invalid value"


@pytest.mark.confirm_payment
class TestPixConfirmation:
    """Testes para confirmação de pagamentos via Pix."""

    def test_pix_confirmation_success(self, client, payment_fixture, mocker):
        """Testa fluxo completo de pagamento confirmado, incluindo evento SocketIO."""
        mock_emit = mocker.patch("sample.payment.src.app.socketio.emit")

        response = client.post(
            "/payments/pix/confirmation",
            json={
                "bank_payment_id": payment_fixture.bank_payment_id,
                "value": payment_fixture.value,
            },
        )

        assert response.status_code == 200
        assert response.json["message"] == "The payment has been confirmed."

        with client.application.app_context():
            updated_payment = Payment.query.get(payment_fixture.id)
            assert updated_payment.paid is True

        mock_emit.assert_called_once_with(f"payment-confirmed-{payment_fixture.id}")

    def test_pix_confirmation_missing_data(self, client):
        """Testa requisição sem 'bank_payment_id' ou 'value'."""
        response = client.post("/payments/pix/confirmation", json={})
        assert response.status_code == 400
        assert response.json["message"] == "Invalid payment data."

    def test_pix_confirmation_invalid_value(self, client, payment_fixture):
        """Testa caso o valor do pagamento não corresponda ao registrado."""
        response = client.post(
            "/payments/pix/confirmation",
            json={
                "bank_payment_id": payment_fixture.bank_payment_id,
                "value": str(payment_fixture.value),
            },
        )
        assert response.status_code == 400
        assert response.json["message"] == "Invalid payment data."

    def test_pix_confirmation_payment_not_found(self, client):
        """Testa caso o pagamento não seja encontrado ou já esteja pago."""
        response = client.post(
            "/payments/pix/confirmation",
            json={"bank_payment_id": "non_existent_id", "value": 100},
        )
        assert response.status_code == 404
        assert response.json["message"] == "Payment not found."

    def test_pix_confirmation_already_paid(self, client, payment_fixture):
        """Testa caso o pagamento já tenha sido confirmado anteriormente."""
        with client.application.app_context():
            Payment.query.filter_by(id=payment_fixture.id).update({"paid": True})
            db.session.commit()
            updated_payment = Payment.query.get(payment_fixture.id)
            assert (
                updated_payment.paid is True
            ), "Erro: O pagamento não foi marcado como pago corretamente no banco"

        response = client.post(
            "/payments/pix/confirmation",
            json={
                "bank_payment_id": payment_fixture.bank_payment_id,
                "value": payment_fixture.value,
            },
        )
        assert response.status_code == 404
        assert response.json["message"] == "Payment not found."


@pytest.mark.get_qrcode_image
class TestGetImage:
    """Testes para obtenção de QR Code."""

    def test_get_image(self, client, payment_fixture):
        file_name = payment_fixture.qr_code
        response = client.get(f"/payments/pix/qr_code/{file_name}")
        assert response.status_code in [200, 404]


@pytest.mark.get_pix_page
class TestPaymentPixPage:
    """Testes para a visualização de um pagamento via Pix."""

    def test_payment_pix_page_not_found(self, client):
        response = client.get("/payments/pix/99999")
        assert response.status_code == 200
        assert "não encontramos seu pedido".encode("utf-8") in response.data

    def test_payment_pix_page_confirmed(self, client, payment_fixture):
        with client.application.app_context():
            Payment.query.filter_by(id=payment_fixture.id).update({"paid": True})
            db.session.commit()

        response = client.get(f"/payments/pix/{payment_fixture.id}")

        print(response.data.decode("utf-8"))

        assert response.status_code == 200
        assert b"Tudo certo com o seu pedido" in response.data

    def test_payment_pix_page_pending(self, client, payment_fixture):
        response = client.get(f"/payments/pix/{payment_fixture.id}")
        assert response.status_code == 200
        assert b"Pedido realizado" in response.data
