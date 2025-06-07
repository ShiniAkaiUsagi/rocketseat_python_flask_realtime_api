import uuid
from pathlib import Path

import qrcode

BASE_DIR = Path.cwd() / "sample" / "payment" / "src"


class Pix:
    def __init__(self):
        pass

    def create_payment(self):
        # Cria o pagamento na 'instituição financeira'.
        # Exemplo criando infos localmente, apenas para prática em aula

        bank_payment_id = uuid.uuid4()
        hash_payment = f"hash_payment_{bank_payment_id}"
        img = qrcode.make(hash_payment)

        img_file_name = f"qr_code_payment_{bank_payment_id}.png"
        img.save(BASE_DIR / "static" / "img" / img_file_name)

        return {"bank_payment_id": bank_payment_id, "qr_code_path": img_file_name}
