import base64
import qrcode

from io import BytesIO
from PIL import Image, ImageFont, ImageDraw

from pkg_resources import resource_stream


def get_qr_with_text(qr, descr):
    dsi = get_qr_text(qr.size, descr)
    resimg = get_concat(qr, dsi)
    return get_img_b64(resimg)


def get_qr(text, **kwargs):
    qr = qrcode.QRCode(**kwargs)
    qr.add_data(text)
    qr.make(fit=True)
    img = qr.make_image()
    img = img.get_image()
    return img


def get_img_b64(img):
    stream = BytesIO()
    img.save(stream, format='png')
    return str(base64.b64encode(stream.getvalue()), encoding='ascii')


def get_qr_text(max_size, text, font='TahomaBold'):
    font_size = 56
    tmpimg = Image.new('L', max_size, 'white')
    text_too_large = True
    while text_too_large:
        file_path = resource_stream(__name__, 'fonts/{}.ttf'.format(font))
        try:
            fnt = ImageFont.truetype(file_path, font_size)
        except Exception:
            fnt = ImageFont.load_default()

        dims = fnt.getbbox(text)
        w, h = (dims[2] - dims[0]), (dims[3] - dims[1])
        if w < max_size[0] - 4 and h < max_size[1] - 4:
            text_too_large = False
        font_size -= 1

    img = Image.new('L', (w, h), 'white')
    draw = ImageDraw.Draw(img)
    draw.text((0, 0), text, font=fnt, fill='black')
    return img


def get_concat(im1, im2, direction='right'):
    if direction == 'right' or direction == 'left':
        width = im1.width + im2.width
        height = max(im1.height, im2.height)
    elif direction == 'down' or direction == 'up':
        width = max(im1.width, im2.width)
        height = im1.height + im2.height
    else:
        raise ValueError(
            'Invalid direction "{}" (must be one of "left", "right", "up", or "down")'.format(direction)
        )

    dst = Image.new('L', (width, height), 'white')

    if direction == 'right' or direction == 'left':
        if im1.height > im2.height:
            im1_y = 0
            im2_y = abs(im1.height-im2.height) // 2
        else:
            im1_y = abs(im1.height-im2.height) // 2
            im2_y = 0

        if direction == 'right':
            im1_x = 0
            im2_x = im1.width
        else:
            im1_x = im2.width
            im2_x = 0
    elif direction == 'up' or direction == 'down':
        if im1.width > im2.width:
            im1_x = 0
            im2_x = abs(im1.width-im2.width) // 2
        else:
            im1_x = abs(im1.width-im2.width) // 2
            im2_x = 0

        if direction == 'down':
            im1_y = 0
            im2_y = im1.height
        else:
            im1_y = im2.height
            im2_y = 0
    else:
        raise ValueError(
            'Invalid direction "{}" (must be one of "left", "right", "up", or "down")'.format(direction)
        )

    dst.paste(im1, (im1_x, im1_y))
    dst.paste(im2, (im2_x, im2_y))

    return dst
