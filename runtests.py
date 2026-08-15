#!/usr/bin/env python3
"""
Standalone test runner for netbox_qrcode.

The plugin's label generation logic is pure Python plus Django template rendering,
so it can be tested without a NetBox installation, a database, or Redis. This
runner supplies the small amount of scaffolding NetBox would otherwise provide
(a `netbox.plugins` module and Django settings), then runs the test suite.

    python runtests.py            # run everything
    python runtests.py -v         # verbose

Inside a real NetBox installation the same tests can be run through NetBox itself,
which supplies the real `netbox.plugins` and settings:

    ./manage.py test netbox_qrcode.tests
"""
import os
import sys
import types
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))


def install_netbox_stub():
    """
    Provide a minimal stand-in for `netbox.plugins` when NetBox is not installed.

    Only the two classes the plugin imports are needed. PluginTemplateExtension
    mirrors the real implementation's constructor and render() behaviour so that
    tests exercise the same code path as NetBox does.
    """
    try:
        import netbox.plugins  # noqa: F401
        return False
    except ImportError:
        pass

    from django.template.loader import get_template

    class PluginConfig:
        pass

    class PluginTemplateExtension:
        models = None

        def __init__(self, context):
            self.context = context

        def render(self, template_name, extra_context=None):
            if extra_context is None:
                extra_context = {}
            elif not isinstance(extra_context, dict):
                raise TypeError("extra_context must be a dictionary")
            return get_template(template_name).render({**self.context, **extra_context})

    netbox = types.ModuleType('netbox')
    netbox.__path__ = []
    plugins = types.ModuleType('netbox.plugins')
    plugins.PluginConfig = PluginConfig
    plugins.PluginTemplateExtension = PluginTemplateExtension
    netbox.plugins = plugins
    sys.modules['netbox'] = netbox
    sys.modules['netbox.plugins'] = plugins
    return True


def configure_django():
    """Configure Django with the plugin's template directory, if not already done."""
    import django
    from django.conf import settings

    if settings.configured:
        return

    class ReleaseInfo:
        """Stand-in for netbox.utilities.release.ReleaseInfo."""
        version = '4.7.0'
        full_version = '4.7.0'

    settings.configure(
        DEBUG=True,
        RELEASE=ReleaseInfo(),
        INSTALLED_APPS=[],
        DATABASES={},
        TEMPLATES=[{
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [os.path.join(HERE, 'netbox_qrcode', 'templates')],
            'APP_DIRS': False,
            'OPTIONS': {'context_processors': []},
        }],
        USE_TZ=True,
    )
    django.setup()


def main():
    sys.path.insert(0, HERE)
    configure_django()
    stubbed = install_netbox_stub()
    print(f"netbox.plugins: {'stubbed (NetBox not installed)' if stubbed else 'real'}")

    verbosity = 2 if '-v' in sys.argv or '--verbose' in sys.argv else 1
    suite = unittest.TestLoader().discover(
        start_dir=os.path.join(HERE, 'netbox_qrcode', 'tests'),
        top_level_dir=HERE,
    )
    # A plain unittest runner is used rather than Django's DiscoverRunner, which
    # would attempt to create a test database the suite does not need.
    result = unittest.TextTestRunner(verbosity=verbosity).run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    sys.exit(main())
