from netbox.plugins import PluginConfig
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
        'title': '',
        'with_text': True,
        'with_qr': True,
        'text_fields': ['name', 'serial'],
        'font': 'TahomaBold',
        'font_size': '3mm',
        'font_weight': 'normal',
        'custom_text': None,
        'text_location': 'right',

        #'url_template': 'Device-{{ obj.name }}',

        # These parameters are used to create the QR code image file.
        'qr_version': 1, # The higher the value, the more boxes you get.
        'qr_error_correction': 0,
        'qr_box_size': 4, # The smaller the number of pixels, the blurrier the QR code will be if the label dimensions are too large, but the quicker the QR code will be ready.
        'qr_border': 0,

        # Parameters for the label (Horizontal)
        'label_qr_width': '12mm',
        'label_qr_height': '12mm',
        'label_qr_text_distance': '1mm',
        'label_width': '56mm',
        'label_height': '32mm',
        'label_edge_top': '0mm',
        'label_edge_left': '1.5mm',
        'label_edge_right': '1.5mm',
        'label_edge_bottom': '0mm',

        # Module-dependent configuration
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
        },

        'powerfeed': {
            'text_fields': ['name'],
        },

        'powerpanel': {
            'text_fields': ['name']
        },  

#####################

        'device_2': {
            'with_qr': False,
            'text_location': 'center',
            'title': 'Example',
            'text_template': '<div style="display: inline-block; height: 5mm; width: 15mm"><img src="/static/netbox_logo.svg" height="100%" width="100%"></div><br>'
                             '{{ obj.name }} <br>'
                             '<div style="display: inline-block; height: 10mm; width: 10mm"><img src="data:image/png;base64,{{qrCode}}" height="100%" width="100%"/></div><br>' 
                             'Device: {{ obj.id|stringformat:"07d" }}'
                             '<p>&#128541; <font color="red"><b> My label design </b> </font> &#128541;</p>',
                             
            'label_width': '56mm',
            'label_height': '32mm',
            'label_edge_top': '0mm',
            'label_edge_left': '0mm',
            'label_edge_right': '0mm',
        },
        
################


    }

config = QRCodeConfig # noqa E305
