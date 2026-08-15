"""Tests for QR code generation, URL derivation, and end-to-end label rendering."""
import base64
import re
import unittest

from netbox_qrcode import template_content as tc
from netbox_qrcode.template_content_functions import create_QRCode, create_url
from netbox_qrcode.utilities import get_img_b64, get_qr

from .base import (
    FakeAsset,
    FakeCable,
    FakeDevice,
    config_for,
    default_config,
    make_extension,
)

PNG_MAGIC = b'\x89PNG\r\n\x1a\n'


def label_count(html):
    """Number of rendered label panels, identified by their print-area element ids."""
    return len(set(re.findall(r'id="QRCode_PrintArea_(\d+)"', html)))


class QRCodeGenerationTest(unittest.TestCase):

    def test_get_qr_returns_an_image(self):
        image = get_qr('https://example.com/', version=1, box_size=4, border=0)
        self.assertTrue(hasattr(image, 'save'))

    def test_get_img_b64_returns_decodable_png(self):
        image = get_qr('https://example.com/', version=1, box_size=4, border=0)
        encoded = get_img_b64(image)
        decoded = base64.b64decode(encoded, validate=True)
        self.assertTrue(decoded.startswith(PNG_MAGIC))

    def test_create_qrcode_passes_only_qr_prefixed_parameters(self):
        # A stray non-qr_ parameter would be forwarded to qrcode.QRCode() and raise.
        config = default_config()
        config['label_width'] = '56mm'
        encoded = create_QRCode('https://example.com/', config)
        self.assertTrue(base64.b64decode(encoded, validate=True).startswith(PNG_MAGIC))

    def test_larger_box_size_produces_larger_image(self):
        small = create_QRCode('https://example.com/', {'qr_version': 1, 'qr_box_size': 2})
        large = create_QRCode('https://example.com/', {'qr_version': 1, 'qr_box_size': 8})
        self.assertGreater(len(large), len(small))


class CreateUrlTest(unittest.TestCase):

    def test_defaults_to_absolute_url_of_object(self):
        extension = make_extension(tc.DeviceQRCode, FakeDevice())
        self.assertEqual(
            create_url(extension, default_config(), FakeDevice()),
            'https://netbox.example.com/dcim/devices/1/',
        )

    def test_url_template_overrides_object_url(self):
        config = default_config()
        config['url_template'] = '{{ obj.name }}|{{ obj.serial }}'
        extension = make_extension(tc.DeviceQRCode, FakeDevice())
        self.assertEqual(
            create_url(extension, config, FakeDevice()),
            'switch-01|SN12345',
        )


class LabelRenderTest(unittest.TestCase):

    def test_device_label_contains_text_and_qr_image(self):
        extension = make_extension(tc.DeviceQRCode, FakeDevice(), config_for('device'))
        html = extension.right_page()
        self.assertIn('switch-01', html)
        self.assertIn('SN12345', html)
        self.assertIn('data:image/png;base64,', html)

    def test_cable_label_renders_on_the_left_page(self):
        extension = make_extension(tc.CableQRCode, FakeCable(), config_for('cable'))
        html = extension.left_page()
        self.assertIn('Gi0/1', html)
        self.assertIn('Gi0/2', html)

    def test_cable_label_contains_no_python_repr(self):
        # Issue #139 surfaced in the rendered HTML, so assert there too.
        extension = make_extension(tc.CableQRCode, FakeCable(), config_for('cable'))
        html = extension.left_page()
        for marker in ('&lt;Interface', '<Interface', '[&lt;', '[<Interface'):
            self.assertNotIn(marker, html)

    def test_title_is_rendered_in_the_panel_heading(self):
        config = config_for('device', title='Asset Label')
        html = make_extension(tc.DeviceQRCode, FakeDevice(), config).right_page()
        self.assertIn('Asset Label', html)

    def test_qr_only_label_omits_text(self):
        config = config_for('device', with_text=False, with_qr=True)
        html = make_extension(tc.DeviceQRCode, FakeDevice(), config).right_page()
        self.assertIn('data:image/png;base64,', html)
        self.assertNotIn('switch-01', html)

    def test_text_only_label_omits_qr_image(self):
        config = config_for('device', with_text=True, with_qr=False)
        html = make_extension(tc.DeviceQRCode, FakeDevice(), config).right_page()
        self.assertIn('switch-01', html)
        self.assertNotIn('data:image/png;base64,', html)


class MultipleLabelTest(unittest.TestCase):
    """
    Regression tests for issue #140, asserted end to end.

    An additional label configuration must produce an additional rendered panel.
    """

    def render(self, extension_class, config, method='right_page'):
        extension = make_extension(extension_class, FakeDevice(), config)
        return getattr(extension, method)()

    def test_single_label_by_default(self):
        self.assertEqual(label_count(self.render(tc.DeviceQRCode, default_config())), 1)

    def test_device_second_label_is_rendered(self):
        config = default_config()
        config['device_2'] = {'title': 'SECOND'}
        html = self.render(tc.DeviceQRCode, config)
        self.assertEqual(label_count(html), 2)
        self.assertIn('SECOND', html)

    def test_asset_second_label_is_rendered(self):
        config = default_config()
        config['asset_2'] = {'title': 'SECOND'}
        extension = make_extension(tc.AssetQRCode, FakeAsset(), config)
        html = extension.right_page()
        self.assertEqual(label_count(html), 2)
        self.assertIn('SECOND', html)

    def test_chain_continues_past_the_second_label(self):
        config = default_config()
        config['asset_2'] = {'title': 'L2'}
        config['asset_3'] = {'title': 'L3'}
        extension = make_extension(tc.AssetQRCode, FakeAsset(), config)
        html = extension.right_page()
        self.assertEqual(label_count(html), 3)
        self.assertIn('L2', html)
        self.assertIn('L3', html)

    def test_chain_stops_at_a_gap_in_the_numbering(self):
        # Documented behaviour: the loop breaks at the first missing increment.
        config = default_config()
        config['device_3'] = {'title': 'L3'}
        html = self.render(tc.DeviceQRCode, config)
        self.assertEqual(label_count(html), 1)
        self.assertNotIn('L3', html)

    def test_supports_up_to_ten_labels(self):
        config = default_config()
        for i in range(2, 11):
            config[f'device_{i}'] = {'title': f'L{i}'}
        self.assertEqual(label_count(self.render(tc.DeviceQRCode, config)), 10)


if __name__ == '__main__':
    unittest.main()
