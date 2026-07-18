import qrcode
import tempfile


def generate_qr(network, address, amount):

    if network == "BTC":
        qr_data = f"bitcoin:{address}?amount={amount:.8f}"

    elif network == "ETH":
        qr_data = f"ethereum:{address}?value={amount:.8f}"

    elif network == "USDT TRC20":
        qr_data = address

    elif network == "USDT ERC20":
        qr_data = f"ethereum:{address}"

    elif network == "USDC ERC20":
        qr_data = f"ethereum:{address}"

    else:
        qr_data = address
        
    print("QR DATA:", qr_data)   

    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=4,
    )

    qr.add_data(qr_data)
    qr.make(fit=True)

    image = qr.make_image(fill_color="black", back_color="white")

    temp = tempfile.NamedTemporaryFile(
        suffix=".png",
        delete=False
    )

    image.save(temp.name)

    return temp.name
