import qrcode
import tempfile


def generate_qr(address):
    qr = qrcode.make(address)

    temp = tempfile.NamedTemporaryFile(
        suffix=".png",
        delete=False
    )

    qr.save(temp.name)

    return temp.name
