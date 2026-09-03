"""
Shared fixtures for the test suite.

The plugin reads attributes off whatever object NetBox is rendering, so the tests
use lightweight stand-ins rather than real NetBox models. Each defines __repr__ in
the same shape Django models use (`<ClassName: str(self)>`), because that repr is
exactly what leaked onto cable labels in issue #139 — a stand-in without it would
not reproduce the bug.
"""
from netbox_qrcode import QRCodeConfig


def default_config():
    """A fresh copy of the plugin's shipped defaults."""
    return dict(QRCodeConfig.default_settings)


def config_for(model_key, **overrides):
    """Defaults with a module-dependent block flattened in, as config_for_modul does."""
    config = default_config()
    config.update(config.get(model_key) or {})
    config.update(overrides)
    return config


class FakeUser:
    def __str__(self):
        return 'admin'


class FakeRequest:
    """
    Stand-in for the HttpRequest placed in the template extension context.

    NetBox 4.7 began passing a sanitized request to custom link templates, but
    template extensions still receive the full request, so build_absolute_uri()
    remains available. This fixture deliberately provides it.
    """
    path = '/dcim/devices/1/'
    path_info = '/dcim/devices/1/'
    method = 'GET'
    GET = {}
    id = 'e4d2c0f6-0000-0000-0000-000000000000'

    def __init__(self):
        self.user = FakeUser()

    def build_absolute_uri(self, location):
        return f'https://netbox.example.com{location}'


class FakeDevice:
    def __init__(self, name='switch-01', serial='SN12345', **extra):
        self.name = name
        self.serial = serial
        for key, value in extra.items():
            setattr(self, key, value)

    def get_absolute_url(self):
        return '/dcim/devices/1/'

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'<Device: {self.name}>'


class FakeInterface:
    def __init__(self, name, device=None):
        self.name = name
        self.device = device

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'<Interface: {self.name}>'


class FakeCable:
    """
    Stand-in for dcim.Cable.

    a_terminations and b_terminations are lists, as they have been since NetBox
    3.3. The pre-3.3 attributes (termination_a and friends) are deliberately
    absent, so that tests confirm stale configuration entries are skipped.
    """
    def __init__(self, a_terminations=None, b_terminations=None):
        device = FakeDevice()
        if a_terminations is None:
            a_terminations = [FakeInterface('Gi0/1', device)]
        if b_terminations is None:
            b_terminations = [FakeInterface('Gi0/2', device)]
        self.a_terminations = a_terminations
        self.b_terminations = b_terminations
        self.label = 'CABLE-1'

    def get_absolute_url(self):
        return '/dcim/cables/1/'

    def __str__(self):
        return 'Cable 1'

    def __repr__(self):
        return '<Cable: Cable 1>'


class FakeAsset:
    """Stand-in for a netbox_inventory.Asset."""
    def __init__(self):
        self.name = 'spare-01'
        self.asset_tag = 'ASSET-9'
        self.serial = 'SN99999'

    def get_absolute_url(self):
        return '/plugins/inventory/assets/1/'

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'<Asset: {self.name}>'


def make_extension(extension_class, obj, config=None):
    """
    Instantiate a PluginTemplateExtension with the context NetBox would supply.

    The context keys mirror those documented on PluginTemplateExtension: object,
    request, config, and settings.
    """
    from django.conf import settings

    return extension_class({
        'object': obj,
        'request': FakeRequest(),
        'config': default_config() if config is None else config,
        'settings': settings,
    })
