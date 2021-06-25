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


def get_qr_text(size, text, font='ArialMT', font_size=100):
    img = Image.new('L', size, 'white')
    flag = True
    while flag:
        file_path = resource_stream(__name__, 'fonts/{}.ttf'.format(font))
        try:
            fnt = ImageFont.truetype(file_path,font_size)
        except Exception:
            fnt = ImageFont.load_default()
            flag = False

        draw = ImageDraw.Draw(img)
        w, h = draw.textsize(text, font=fnt)
        if w < size[0] - 4 and h < size[1] - 4:
            flag = False
        font_size -= 1
    W, H = size
    draw.text(((W-w)/2, (H-h)/2), text, font=fnt, fill='black')

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


def get_concat_v(im1, im2):
    dst = Image.new('L', (im1.width, im1.height + im2.height), 'white')
    dst.paste(im1, (0, 0))
    dst.paste(im2, (0, im1.height))
    return dst


def add_print_padding_left(img, padding):
    blank = Image.new('L', (padding, img.height), 'white')
    img = get_concat(blank, img)
    return img


def add_print_padding_v(img, padding):
    blank = Image.new('L', (img.width, padding), 'white')
    img = get_concat_v(blank, img)
    img = get_concat_v(img, blank)
    return img