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
    overlay_alpha: float | None = None,
    **kwargs,
):
    qr = qrcode.QRCode(**kwargs)
    qr.add_data(text)
    qr.make(fit=True)
    img = qr.make_image()
    img = img.get_image()
    if overlay:
        img = texture_qr_modules(img, overlay, overlay_alpha)
    return img


##################################
# Converts an image to Base64
# --------------------------------
# Parameter:
#   img: Image file
def get_img_b64(img):
    stream = BytesIO()
    img.save(stream, format="png")
    return str(base64.b64encode(stream.getvalue()), encoding="ascii")


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
    overlay_alpha: float | None = None,
) -> Image.Image:
    """
    Replace the QR Code's black modules with pixels from 'texture_path',
    leaving white background untouched. Transparent pixels in the texture are not affected.
    """

    qr_rgb = qr_img.convert("RGB")

    inv = ImageOps.invert(qr_rgb.convert("L"))
    mask = inv.point(lambda p: 255 if p > 128 else 0)

    # Load texture in RGBA to detect transparent pixels
    texture = (
        Image.open(texture_path).convert("RGBA").resize(qr_rgb.size, Image.LANCZOS)
    )

    # Extract alpha channel
    alpha = texture.split()[3]

    # Adjust alpha transparency if overlay_alpha is provided
    if overlay_alpha is not None:
        alpha = alpha.point(lambda p: int(p * overlay_alpha))

    texture_rgb = texture.convert("RGB")

    # Composite texture over the original QR using alpha channel
    result = Image.composite(texture_rgb, qr_rgb, alpha)

    # Now apply the QR mask to keep white background, only allowing texture in black modules
    white = Image.new("RGB", qr_rgb.size, (255, 255, 255))
    textured_modules = Image.composite(result, white, mask)

    return textured_modules
