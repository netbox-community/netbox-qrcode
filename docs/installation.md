# Installation

This plugin is installed like any other NetBox plugin. It requires no database migrations and adds no models.

!!! note
    Check the [compatibility matrix](https://github.com/netbox-community/netbox-qrcode/blob/main/COMPATIBILITY.md) before installing, and choose a plugin release which supports your NetBox version.

## 1. Virtual Environment

The plugin is distributed on [PyPI](https://pypi.org/project/netbox-qrcode/). If NetBox was installed following the standard installation instructions, first activate its Python virtual environment (typically located at `/opt/netbox/venv/`):

```
source /opt/netbox/venv/bin/activate
```

!!! note
    You may need to modify the `source` command above if your virtual environment has been installed in a different location.

## 2. Python Package

Use `pip` to install the Python package:

```
pip install netbox-qrcode
```

The [qrcode](https://github.com/lincolnloop/python-qrcode) and [Pillow](https://github.com/python-pillow/Pillow) libraries are installed automatically as dependencies.

## 3. Enable Plugin

Add `netbox_qrcode` to the `PLUGINS` list in `configuration.py`, which is normally located at `/opt/netbox/netbox/netbox/configuration.py`:

```python
PLUGINS = [
    # ...
    'netbox_qrcode',
]
```

!!! note
    If there are no plugins already installed, you might need to create this parameter. If so, be sure to define `PLUGINS` as a list _containing_ the plugin name as above, rather than just the name.

## 4. Persist the Installation

Add the package to `local_requirements.txt` so that it is reinstalled automatically when NetBox is upgraded:

```
echo netbox-qrcode >> /opt/netbox/local_requirements.txt
```

!!! warning
    Skipping this step means the plugin will be missing after the next NetBox upgrade, and NetBox will fail to start because `configuration.py` still references it.

## 5. Restart NetBox

Restart the NetBox services to load the plugin:

```
sudo systemctl restart netbox netbox-rq
```

No migrations are required. QR code panels should now appear on the detail views of the supported object types.

## 6. Configure (Optional)

The plugin works with no configuration at all, using its built-in defaults. To customise label dimensions, text, fonts, or to define additional label designs, add a `netbox_qrcode` block to `PLUGINS_CONFIG`:

```python
PLUGINS_CONFIG = {
    'netbox_qrcode': {
        'label_width': '56mm',
        'label_height': '32mm',
    }
}
```

See the [configuration reference](configuration.md) for the full list of parameters, and the [label examples](label-examples.md) for designs you can copy.

## Optional: netbox-inventory Support

If [netbox-inventory](https://github.com/ArnesSI/netbox-inventory) is installed, QR code labels are also rendered on Asset detail views automatically. No additional configuration is required to enable this; the plugin detects netbox-inventory at startup and registers the Asset view only when it is present.

Asset labels are configured under the `asset` key:

```python
PLUGINS_CONFIG = {
    'netbox_qrcode': {
        'asset': {
            'text_fields': ['name', 'asset_tag', 'serial'],
        },
    }
}
```

## Development Environment

A Docker Compose environment is included for plugin development. It builds NetBox from source and mounts the plugin in editable mode:

```
make cbuild
make debug
```

NetBox is then available at `http://localhost:8000`. Use `make adduser` to create a superuser, and `make stop` to shut the environment down. The NetBox version and Python version used are controlled by the `NETBOX_VER` and `PYTHON_VER` variables at the top of the `Makefile`.
