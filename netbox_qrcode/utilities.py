import base64
import qrcode
from io import BytesIO

# ******************************************************************************************
# Includes useful tools to create the content.
# ******************************************************************************************

##################################          
# Creates a QR code as an image.: https://pypi.org/project/qrcode/3.0/
# --------------------------------
# Parameter:
#   text: Text to be included in the QR code.
#   **kwargs: List of parameters which properties the QR code should have. (e.g. version, box_size, error_correction, border etc.)
def get_qr(text, **kwargs):
    qr_kwargs = {key: value for key, value in kwargs.items() if key != 'image_kwargs'}
    qr = qrcode.QRCode(**qr_kwargs)
    qr.add_data(text)
    qr.make(fit=True)

    if 'image_kwargs' in kwargs:
        img = qr.make_image(**kwargs['image_kwargs'])
    else:
        img = qr.make_image()

    img = img.get_image()
    return img

##################################          
# Converts an image to Base64
# --------------------------------
# Parameter:
#   img: Image file
def get_img_b64(img):
    stream = BytesIO()
    img.save(stream, format='png')
    return str(base64.b64encode(stream.getvalue()), encoding='ascii')