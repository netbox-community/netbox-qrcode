
from django.core.exceptions import ObjectDoesNotExist
from extras.plugins import PluginTemplateExtension

from .utilities import get_img_b64, get_qr, get_qr_text, get_concat


class QRCode(PluginTemplateExtension):
    model = 'dcim.device'

    def right_page(self):
        config = self.context['config']
        device = self.context['object']
        request = self.context['request']
        url = request.build_absolute_uri(device.get_absolute_url())
        qr_args = {}
        for k, v in config.items():
            if k.startswith('qr_'):
                qr_args[k.replace('qr_', '')] = v
        qr_img = get_qr(url, **qr_args)
        if config.get('with_text'):
            text = []
            for text_field in config.get('text_fields', []):
                if getattr(device, text_field, None):
                    text.append('{}'.format(getattr(device, text_field)))
            custom_text = config.get('custom_text')
            if custom_text:
                text.append(custom_text)
            text = '\n'.join(text)
            text_img = get_qr_text(qr_img.size, text, config.get('font'))
            qr_with_text = get_concat(qr_img, text_img)
            img = get_img_b64(qr_with_text)
        else:
            img = get_img_b64(qr_img)
        try:
            return self.render(
                'netbox_qrcode/qrcode.html', extra_context={'image': img}
            )
        except ObjectDoesNotExist:
            return ""


template_extensions = [QRCode]
