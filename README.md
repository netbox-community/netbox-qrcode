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

### Set the label printer correctly

If the print does not look like the preview in the Netbox, first try to get a perfect print using Word. As many printer settings also have an influence on the print result. Borderless printing is possible if the printer (e.g. thermal transfer printer) supports this.

![ShowImage](/docs/img/Configuration_Printer_WordPreview.png)


Here is an example of what needs to be considered to print borderless from a Word document. [Go to: Eexample Zebra ZM400 300dpi label printer and a label 56x32mm. >>](/docs/img/Configuration_Printer_ZM400.png)


### Browser Print Settings correctly

When you press the “Print” button, there are some print properties that are added by the browser. However, these interfere with the print result. They should therefore be deactivated.

#### Firefox:

| Parameter                                      | Value                        |
| ---------------------------------------------  | ---------------------------  |
| Orientation                                    | Portrait                     |  
| Paper size                                     | User defined                 |
| Margins                                        | none                         |
| Scale                                          | Fit to page width or 100%    |
| Options --> Print headers and footers          | disable                      |
| Options --> Print backgrounds                  | disable                      |

#### Chrome:
The worst part was finding the right parameters for Chrome. Because it always turned it differently when printing than the print preview shows.
| Parameter                                      | Value                        |
| ---------------------------------------------  | ---------------------------  |
| Layout                                         | Portrait                     |  
| Paper size                                     | empty !!!                    |
| Pages per sheet                                | 1                            |
| Margins                                        | none                         |
| Scale                                          | Default or 100%              |
| Options --> PBackground grafics                | disable                      |

![Image](/docs/img/Configuration_Browser_Print_Settings.png)


### Design your own label

You can customise the label as you wish, even 2 different labels for the ‘Device’ view, for example, are possible.

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