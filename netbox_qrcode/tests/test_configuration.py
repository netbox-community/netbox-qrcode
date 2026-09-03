"""Tests for configuration key derivation and the configuration layering rules."""
import unittest

from netbox_qrcode import template_content as tc
from netbox_qrcode.template_content_functions import config_for_modul, model_config_key

from .base import FakeDevice, default_config, make_extension

# Every template extension the plugin registers, paired with the configuration key
# it is expected to read. AssetQRCode is included even though it is only appended
# to template_extensions when netbox-inventory is installed.
EXTENSIONS = [
    (tc.DeviceQRCode, 'device'),
    (tc.ModuleQRCode, 'module'),
    (tc.RackQRCode, 'rack'),
    (tc.CableQRCode, 'cable'),
    (tc.LocationQRCode, 'location'),
    (tc.PowerFeedQRCode, 'powerfeed'),
    (tc.PowerPanelQRCode, 'powerpanel'),
    (tc.AssetQRCode, 'asset'),
]


class ModelConfigKeyTest(unittest.TestCase):

    def test_strips_dcim_app_label(self):
        self.assertEqual(model_config_key(('dcim.device',)), 'device')

    def test_strips_plugin_app_label(self):
        self.assertEqual(model_config_key(('netbox_inventory.asset',)), 'asset')

    def test_strips_only_the_first_dot(self):
        self.assertEqual(model_config_key(('plugin_x.some.model',)), 'some.model')

    def test_passes_through_value_without_app_label(self):
        self.assertEqual(model_config_key(('nodot',)), 'nodot')

    def test_every_registered_extension_maps_to_expected_key(self):
        for extension_class, expected in EXTENSIONS:
            with self.subTest(extension=extension_class.__name__):
                self.assertEqual(model_config_key(extension_class.models), expected)


class ConfigKeyAgreementTest(unittest.TestCase):
    """
    Regression tests for issue #140.

    Create_PluginContent derives the key it looks up for an additional label, and
    config_for_modul derives the key it reads. These used to disagree for models
    outside dcim, silently disabling additional labels for netbox-inventory assets.
    """

    def test_lookup_and_read_keys_agree_for_every_extension(self):
        for extension_class, key in EXTENSIONS:
            with self.subTest(extension=extension_class.__name__):
                config = default_config()
                config[f'{key}_2'] = {'title': 'PROBE'}
                extension = make_extension(extension_class, FakeDevice(), config)
                resolved = config_for_modul(extension, 2)
                self.assertEqual(
                    resolved.get('title'), 'PROBE',
                    f'config_for_modul did not read {key}_2',
                )

    def test_asset_additional_label_key_is_not_app_label_prefixed(self):
        self.assertEqual(model_config_key(tc.AssetQRCode.models) + '_2', 'asset_2')


class ConfigLayeringTest(unittest.TestCase):

    def resolve(self, extension_class, config, label_no=1):
        extension = make_extension(extension_class, FakeDevice(), config)
        return config_for_modul(extension, label_no)

    def test_defaults_are_returned_when_nothing_overridden(self):
        resolved = self.resolve(tc.DeviceQRCode, default_config())
        self.assertEqual(resolved['label_width'], '56mm')

    def test_global_setting_overrides_default(self):
        config = default_config()
        config['label_width'] = '99mm'
        self.assertEqual(self.resolve(tc.DeviceQRCode, config)['label_width'], '99mm')

    def test_module_block_overrides_global_setting(self):
        config = default_config()
        config['font_size'] = '5mm'
        config['device'] = {'font_size': '10mm'}
        self.assertEqual(self.resolve(tc.DeviceQRCode, config)['font_size'], '10mm')

    def test_module_block_does_not_leak_to_other_object_types(self):
        config = default_config()
        config['device'] = {'font_size': '10mm'}
        config['rack'] = {}
        self.assertEqual(self.resolve(tc.RackQRCode, config)['font_size'],
                         default_config()['font_size'])

    def test_numbered_block_applies_for_that_label_only(self):
        config = default_config()
        config['device_2'] = {'label_width': '25mm'}
        self.assertEqual(self.resolve(tc.DeviceQRCode, config, 1)['label_width'], '56mm')
        self.assertEqual(self.resolve(tc.DeviceQRCode, config, 2)['label_width'], '25mm')

    def test_resolution_does_not_mutate_the_supplied_config(self):
        config = default_config()
        config['device'] = {'font_size': '10mm'}
        self.resolve(tc.DeviceQRCode, config)
        self.assertEqual(config['font_size'], default_config()['font_size'])


class RegisteredExtensionsTest(unittest.TestCase):

    def test_core_extensions_are_registered(self):
        registered = {cls.__name__ for cls in tc.template_extensions}
        self.assertEqual(registered, {
            'DeviceQRCode', 'ModuleQRCode', 'RackQRCode', 'CableQRCode',
            'LocationQRCode', 'PowerFeedQRCode', 'PowerPanelQRCode',
        } | ({'AssetQRCode'} if tc.INVENTORY_AVAILABLE else set()))

    def test_asset_extension_registered_only_with_netbox_inventory(self):
        registered = {cls.__name__ for cls in tc.template_extensions}
        self.assertEqual('AssetQRCode' in registered, tc.INVENTORY_AVAILABLE)

    def test_every_extension_declares_exactly_one_model(self):
        for extension_class, _ in EXTENSIONS:
            with self.subTest(extension=extension_class.__name__):
                self.assertEqual(len(extension_class.models), 1)

    def test_every_extension_has_a_default_config_block(self):
        defaults = default_config()
        for _, key in EXTENSIONS:
            with self.subTest(key=key):
                self.assertIn(key, defaults)


if __name__ == '__main__':
    unittest.main()
