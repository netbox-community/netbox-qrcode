# Change Log

## v1.0.0

### NetBox 4.7 Support

This release targets NetBox 4.7. The supported range is declared as a minimum of 4.7.0 and a maximum of 4.7.99; see the [compatibility matrix](https://github.com/netbox-community/netbox-qrcode/blob/main/COMPATIBILITY.md) for earlier releases.

### Bug Fixes

* [#139](https://github.com/netbox-community/netbox-qrcode/issues/139) - Cable labels rendered raw Python list reprs (for example `[<Interface: Gi0/1>]`) instead of termination names. Multi-value fields are now rendered as a comma-separated list of their values, and the four default `cable` text fields removed from NetBox in v3.3 (`_termination_a_device`, `termination_a`, `_termination_b_device`, `termination_b`) have been dropped from the default configuration.
* [#140](https://github.com/netbox-community/netbox-qrcode/issues/140) - Additional label configurations (`asset_2` through `asset_10`) were unreachable for netbox-inventory assets, because the configuration key was derived inconsistently in two places. Key derivation is now shared, and strips any app label rather than only `dcim.`.

### Housekeeping

* Documentation restructured into an MkDocs site.
* Removed the invalid `min_version` and `max_version` arguments from `setup.py`, which setuptools silently discarded. The supported NetBox range is declared in `PluginConfig`, which is where it takes effect.
* Declared `python_requires='>=3.12'` to match NetBox 4.7's supported Python versions.
* Replaced the deprecated `License ::` classifier with an SPDX `license` declaration, and dropped references to bundled `.ttf` font files, which were removed when label rendering moved to CSS.
* Development environment updated for NetBox 4.7: Redis raised to 7 (4.7 requires Redis 6.0 or later).

---

## Earlier Releases

Releases prior to v1.0.0 predate this change log. See the [GitHub releases page](https://github.com/netbox-community/netbox-qrcode/releases) and the [compatibility matrix](https://github.com/netbox-community/netbox-qrcode/blob/main/COMPATIBILITY.md) for their supported NetBox versions.
