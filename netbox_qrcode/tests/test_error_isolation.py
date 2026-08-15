"""
Tests for per-label error isolation (issue #141).

A label design whose configuration cannot be rendered must not discard the object's
other labels. NetBox core wraps each template extension call in a broad except and
substitutes its own error template, so an exception escaping right_page() costs the
plugin all of its output at once, not just the failing label.
"""
import logging
import re
import unittest

from netbox_qrcode import template_content as tc

from .base import FakeDevice, default_config, make_extension

# A parameter qrcode.QRCode() does not accept, which raises TypeError during render.
BROKEN = {'qr_bogus': 'boom'}


def label_count(html):
    return len(set(re.findall(r'id="QRCode_PrintArea_(\d+)"', html)))


def error_panels(html):
    return len(re.findall(r'could not be rendered', html))


class ErrorIsolationTest(unittest.TestCase):

    def render(self, config):
        return make_extension(tc.DeviceQRCode, FakeDevice(), config).right_page()

    def test_broken_design_does_not_discard_the_others(self):
        # The scenario from the issue: four designs, only the third is broken.
        config = default_config()
        config['device_2'] = {'title': 'L2'}
        config['device_3'] = {'title': 'L3', **BROKEN}
        config['device_4'] = {'title': 'L4'}
        html = self.render(config)
        self.assertEqual(label_count(html), 3)
        self.assertEqual(error_panels(html), 1)
        self.assertIn('L2', html)
        self.assertIn('L4', html)

    def test_error_panel_names_the_failing_config_key(self):
        config = default_config()
        config['device_2'] = {'title': 'L2', **BROKEN}
        html = self.render(config)
        self.assertIn('<code>device_2</code>', html)

    def test_broken_first_design_still_renders_later_designs(self):
        config = default_config()
        config.update(BROKEN)  # breaks the base design, and thus every label
        config['device_2'] = {'title': 'L2'}
        html = self.render(config)
        # Both labels fail here because the broken parameter is global, but the panel
        # must still report both rather than collapsing to nothing.
        self.assertEqual(error_panels(html), 2)
        self.assertIn('<code>device</code>', html)
        self.assertIn('<code>device_2</code>', html)

    def test_only_the_broken_design_fails_when_scoped_to_it(self):
        config = default_config()
        config['device_2'] = {'title': 'L2', **BROKEN}
        html = self.render(config)
        self.assertEqual(label_count(html), 1)
        self.assertEqual(error_panels(html), 1)

    def test_exception_does_not_escape_right_page(self):
        config = default_config()
        config['device_2'] = {'title': 'L2', **BROKEN}
        try:
            self.render(config)
        except Exception as e:  # pragma: no cover
            self.fail(f'{type(e).__name__} escaped right_page(): {e}')

    def test_failure_is_logged_with_the_config_key(self):
        config = default_config()
        config['device_2'] = {'title': 'L2', **BROKEN}
        with self.assertLogs('netbox.plugins.netbox_qrcode', level='WARNING') as captured:
            self.render(config)
        self.assertEqual(len(captured.records), 1)
        self.assertIn('device_2', captured.output[0])
        self.assertIn('TypeError', captured.output[0])

    def test_error_text_is_escaped(self):
        # The exception repr is user-supplied config, so it must not inject markup.
        config = default_config()
        config['device_2'] = {'title': 'L2', 'qr_<script>alert(1)</script>': 'x'}
        html = self.render(config)
        self.assertNotIn('<script>alert(1)</script>', html)
        self.assertIn('&lt;script&gt;', html)

    def test_healthy_config_produces_no_error_panels(self):
        config = default_config()
        config['device_2'] = {'title': 'L2'}
        html = self.render(config)
        self.assertEqual(label_count(html), 2)
        self.assertEqual(error_panels(html), 0)


class TemplateErrorIsolationTest(unittest.TestCase):
    """Other realistic misconfigurations named in the issue."""

    def render(self, overrides):
        config = default_config()
        config['device_2'] = {'title': 'L2', **overrides}
        return make_extension(tc.DeviceQRCode, FakeDevice(), config).right_page()

    def test_malformed_text_template_is_isolated(self):
        html = self.render({'text_template': '{% invalid_tag %}'})
        self.assertEqual(label_count(html), 1)
        self.assertEqual(error_panels(html), 1)

    def test_malformed_url_template_is_isolated(self):
        html = self.render({'url_template': '{% nope %}'})
        self.assertEqual(label_count(html), 1)
        self.assertEqual(error_panels(html), 1)

    def test_out_of_range_qr_version_is_isolated(self):
        html = self.render({'qr_version': 99})
        self.assertEqual(label_count(html), 1)
        self.assertEqual(error_panels(html), 1)


class ConfigNameTest(unittest.TestCase):

    def test_first_label_uses_the_bare_model_key(self):
        extension = make_extension(tc.DeviceQRCode, FakeDevice())
        self.assertEqual(extension.Config_Name(1), 'device')

    def test_later_labels_are_suffixed(self):
        extension = make_extension(tc.DeviceQRCode, FakeDevice())
        self.assertEqual(extension.Config_Name(2), 'device_2')
        self.assertEqual(extension.Config_Name(10), 'device_10')

    def test_plugin_models_are_not_app_label_prefixed(self):
        extension = make_extension(tc.AssetQRCode, FakeDevice())
        self.assertEqual(extension.Config_Name(2), 'asset_2')


if __name__ == '__main__':
    unittest.main()
