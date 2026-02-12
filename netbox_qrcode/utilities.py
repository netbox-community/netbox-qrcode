import base64
import qrcode
from io import BytesIO
from PIL import Image, ImageOps, ImageEnhance

# ******************************************************************************************
# Includes useful tools to create the content.
# ******************************************************************************************

##################################          
# Creates a QR code as an image.: https://pypi.org/project/qrcode/3.0/
# --------------------------------
# Parameter:
#   text: Text to be included in the QR code.
#   **kwargs: List of parameters which properties the QR code should have. (e.g. version, box_size, error_correction, border etc.)
def get_qr(
    text,
    overlay: str | None = None,
    overlay_brightness_enhance: float | None = None,
    **kwargs,
):
    qr = qrcode.QRCode(**kwargs)
    qr.add_data(text)
    qr.make(fit=True)
    img = qr.make_image()
    img = img.get_image()
    if overlay:
        img = texture_qr_modules(img, overlay, overlay_brightness_enhance)
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

##################################
# Replace the QR Code's black modules with pixels from 'texture_path',
# leaving white background untouched.
# --------------------------------
# Parameter:
#   qr_img: Generated QR code
#   texture_path: Path to overlay image
#   brightness_enhance: Float of 0-1 to increase brightness
def texture_qr_modules(
    qr_img: Image.Image,
    texture_path: str,
    overlay_brightness_enhance: float | None = None,
) -> Image.Image:
    """
    Replace the QR Code's black modules with pixels from 'texture_path',
    leaving white background untouched.
    """

    qr_rgb = qr_img.convert("RGB")

    inv = ImageOps.invert(qr_rgb.convert("L"))
    mask = inv.point(lambda p: 255 if p > 128 else 0)

    texture = Image.open(texture_path).convert("RGB").resize(qr_rgb.size, Image.LANCZOS)

    if overlay_brightness_enhance:
        texture = ImageEnhance.Brightness(texture).enhance(overlay_brightness_enhance)

    white = Image.new("RGB", qr_rgb.size, (255, 255, 255))
    textured_modules = Image.composite(texture, white, mask)

    return textured_modules


