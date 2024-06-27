import pyqrcode
from pyqrcode import QRCode
img = QRCode.make("I love python")
img.save("qrcode.png")
