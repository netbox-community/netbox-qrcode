from extras.plugins import PluginConfig
from .version import __version__


class QRCodeConfig(PluginConfig):
    name = 'netbox_qrcode'
    verbose_name = 'qrcode'
    description = 'Generate QR codes for the objects'
    version = __version__
    author = 'Nikolay Yuzefovich'
    author_email = 'mgk.kolek@gmail.com'
    required_settings = []
    default_settings = {
        'with_text': True,
        'text_fields': ['name', 'serial'],
        'font': 'TahomaBold',
        'custom_text': None,
        'text_location': 'right',
        'qr_version': 1,
        'qr_error_correction': 0,
        'qr_box_size': 6,
        'qr_border': 4,
        'device': {
            'text_fields': ['name', 'serial']
        },
        'rack': {
            'text_fields': ['name']
        },
        'cable': {
            'text_fields': [
                '_termination_a_device',
                'termination_a',
                '_termination_b_device',
                'termination_b',
                'a_terminations.device',
                'a_terminations',
                'b_terminations.device',
                'b_terminations'
                ]
        },
        'location': {
            'text_fields': ['name']
        }
    }

config = QRCodeConfig # noqa E305
