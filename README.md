# Netbox QR Code Plugin

[Netbox](https://github.com/netbox-community/netbox) plugin for generate QR codes for objects: Rack, Device, Cable.

This plugin depends on [qrcode](https://github.com/lincolnloop/python-qrcode) and [Pillow](https://github.com/python-pillow/Pillow) python library

[![Downloads](https://static.pepy.tech/badge/netbox-qrcode)](https://pepy.tech/project/netbox-qrcode)
[![Downloads](https://static.pepy.tech/badge/netbox-qrcode/month)](https://pepy.tech/project/netbox-qrcode)
[![Downloads](https://static.pepy.tech/badge/netbox-qrcode/week)](https://pepy.tech/project/netbox-qrcode)

## Compatibility

| Plugin Version | NetBox Version | Tested on                      |
| ------------- |:-------------| :-----:|
| 0.0.11          | >= 3.7.0        | 3.7.x |
| 0.0.13          | >= 4.0.2        | v4.0.2                   |

Netbox version 2 is no longer supported.

## Installation

If Netbox was installed according to the standard installation instructions. It may be necessary to activate the virtual environment.

```
source /opt/netbox/venv/bin/activate
```

The plugin is available as a Python package in pypi and can be installed with pip

```
pip install netbox-qrcode
```
Enable the plugin in /opt/netbox/netbox/netbox/configuration.py:
```
PLUGINS = ['netbox_qrcode']
```
Restart NetBox and add `netbox-qrcode` to your local_requirements.txt

## Configuration
Design your own label.

- [Go to Configuration >>](docs/README_Subpages/README_Configuration.md)
- [Go to Example label configurations >>](docs/README_Subpages/README_Configuration_ExampleLabelConf.md)

![Cable QR Code](/docs/img/Configuration_Label_Example_10.png)

## Contributing
Developing tools for this project based on [ntc-netbox-plugin-onboarding](https://github.com/networktocode/ntc-netbox-plugin-onboarding) repo.

Issues and pull requests are welcomed.

## Screenshots

Device QR code with text label
![Device QR Code](docs/img/qrcode.png)

Rack QR code
![Rack QR Code](docs/img/qrcode_rack.png)

Cable QR code
![Cable QR Code](docs/img/qrcode_cable.png)