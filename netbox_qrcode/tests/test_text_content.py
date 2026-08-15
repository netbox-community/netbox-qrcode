"""Tests for label text generation (get_text_fields, create_text, templates)."""
import unittest

from netbox_qrcode.template_content_functions import (
    create_text,
    get_text_fields,
    get_text_template,
)

from .base import FakeCable, FakeDevice, FakeInterface, config_for, default_config


class GetTextFieldsTest(unittest.TestCase):

    def text(self, obj, fields, **overrides):
        config = default_config()
        config['text_fields'] = fields
        config.update(overrides)
        return get_text_fields(config, obj)

    def test_scalar_fields_joined_with_line_breaks(self):
        self.assertEqual(
            self.text(FakeDevice(), ['name', 'serial']),
            'switch-01<br>SN12345',
        )

    def test_missing_fields_are_skipped(self):
        # A single text_fields list can be shared across object types, so fields
        # which do not exist on the object must not raise.
        self.assertEqual(
            self.text(FakeDevice(), ['name', 'does_not_exist', 'serial']),
            'switch-01<br>SN12345',
        )

    def test_falsy_fields_are_skipped(self):
        self.assertEqual(self.text(FakeDevice(serial=''), ['name', 'serial']), 'switch-01')

    def test_custom_text_appended_last(self):
        self.assertEqual(
            self.text(FakeDevice(), ['name'], custom_text='Property of ACME'),
            'switch-01<br>Property of ACME',
        )

    def test_dotted_lookup_on_plain_related_object_yields_nothing(self):
        # Documents a real limitation: dotted lookup is implemented as .get(key),
        # so it resolves dict-like values and lists, but not attributes of a plain
        # related object. 'site.name' silently contributes nothing; use a template
        # (text_template) to reach across a foreign key.
        obj = FakeDevice()
        obj.site = FakeDevice(name='site-a')
        self.assertEqual(self.text(obj, ['site.name']), '')

    def test_undotted_related_object_renders_its_string_representation(self):
        obj = FakeDevice()
        obj.site = FakeDevice(name='site-a')
        self.assertEqual(self.text(obj, ['site']), 'site-a')

    def test_dotted_lookup_into_custom_field_dict(self):
        obj = FakeDevice(custom_field_data={'rack_unit': 42})
        self.assertEqual(self.text(obj, ['custom_field_data.rack_unit']), '42')

    def test_no_fields_yields_empty_string(self):
        self.assertEqual(self.text(FakeDevice(), []), '')


class MultiValueFieldTest(unittest.TestCase):
    """
    Regression tests for issue #139.

    A bare multi-value attribute used to be formatted with '{}'.format(value),
    which rendered the Python list repr onto the label.
    """

    def text(self, obj, fields):
        config = default_config()
        config['text_fields'] = fields
        return get_text_fields(config, obj)

    def test_single_element_list_renders_value_not_repr(self):
        result = self.text(FakeCable(), ['a_terminations'])
        self.assertEqual(result, 'Gi0/1')
        self.assertNotIn('[', result)
        self.assertNotIn('<Interface', result)

    def test_multiple_elements_are_comma_separated(self):
        cable = FakeCable(a_terminations=[FakeInterface('Gi0/1'), FakeInterface('Gi0/2')])
        self.assertEqual(self.text(cable, ['a_terminations']), 'Gi0/1, Gi0/2')

    def test_empty_list_is_skipped(self):
        cable = FakeCable(a_terminations=[])
        self.assertEqual(self.text(cable, ['a_terminations', 'b_terminations']), 'Gi0/2')

    def test_tuple_is_handled_like_a_list(self):
        cable = FakeCable(a_terminations=(FakeInterface('Gi0/1'),))
        self.assertEqual(self.text(cable, ['a_terminations']), 'Gi0/1')

    def test_dotted_lookup_unwraps_first_list_element(self):
        self.assertEqual(self.text(FakeCable(), ['a_terminations.device']), 'switch-01')

    def test_cable_defaults_contain_no_list_repr(self):
        config = config_for('cable')
        result = get_text_fields(config, FakeCable())
        self.assertEqual(result, 'switch-01<br>Gi0/1<br>switch-01<br>Gi0/2')
        for marker in ('[', ']', '<Interface', '<Device'):
            self.assertNotIn(marker, result)

    def test_cable_defaults_omit_fields_removed_in_netbox_33(self):
        fields = default_config()['cable']['text_fields']
        for removed in ('_termination_a_device', 'termination_a',
                        '_termination_b_device', 'termination_b'):
            self.assertNotIn(removed, fields)

    def test_stale_field_names_in_user_config_still_skipped(self):
        # Users who kept the pre-3.3 names in their own configuration must not break.
        legacy = ['_termination_a_device', 'termination_a',
                  '_termination_b_device', 'termination_b',
                  'a_terminations.device', 'a_terminations',
                  'b_terminations.device', 'b_terminations']
        self.assertEqual(
            self.text(FakeCable(), legacy),
            'switch-01<br>Gi0/1<br>switch-01<br>Gi0/2',
        )


class CreateTextTest(unittest.TestCase):

    def test_returns_none_when_text_disabled(self):
        config = default_config()
        config['with_text'] = False
        self.assertIsNone(create_text(config, FakeDevice(), 'QRB64'))

    def test_uses_text_fields_by_default(self):
        config = config_for('device')
        self.assertEqual(create_text(config, FakeDevice(), 'QRB64'), 'switch-01<br>SN12345')

    def test_text_template_takes_precedence_over_text_fields(self):
        config = config_for('device')
        config['text_template'] = 'ID {{ obj.name }}'
        self.assertEqual(create_text(config, FakeDevice(), 'QRB64'), 'ID switch-01')

    def test_text_template_receives_obj_logo_and_qrcode(self):
        config = default_config()
        config['logo'] = '/media/logo.png'
        config['text_template'] = '{{ obj.name }}|{{ logo }}|{{ qrCode }}'
        self.assertEqual(
            get_text_template(config, FakeDevice(), 'QRB64'),
            'switch-01|/media/logo.png|QRB64',
        )


if __name__ == '__main__':
    unittest.main()
