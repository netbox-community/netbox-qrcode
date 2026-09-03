# Change Log

## v1.0.0

### NetBox 4.7 Support

This release targets NetBox 4.7. The supported range is declared as a minimum of 4.7.0 and a maximum of 4.7.99; see the [compatibility matrix](https://github.com/netbox-community/netbox-qrcode/blob/main/COMPATIBILITY.md) for earlier releases.

### Bug Fixes

* [#139](https://github.com/netbox-community/netbox-qrcode/issues/139) - Cable labels rendered raw Python list reprs (for example `[<Interface: Gi0/1>]`) instead of termination names. Multi-value fields are now rendered as a comma-separated list of their values, and the four default `cable` text fields removed from NetBox in v3.3 (`_termination_a_device`, `termination_a`, `_termination_b_device`, `termination_b`) have been dropped from the default configuration.
* [#140](https://github.com/netbox-community/netbox-qrcode/issues/140) - Additional label configurations (`asset_2` through `asset_10`) were unreachable for netbox-inventory assets, because the configuration key was derived inconsistently in two places. Key derivation is now shared, and strips any app label rather than only `dcim.`.
* [#141](https://github.com/netbox-community/netbox-qrcode/issues/141) - A single misconfigured label design removed every label for that object type, because an exception in any one design propagated out of the template extension and NetBox replaced the plugin's entire output. Each label design is now rendered in isolation: a design which fails is replaced by a panel naming the configuration key at fault, the failure is logged as a warning under `netbox.plugins.netbox_qrcode`, and the object's remaining labels render as normal.

### Housekeeping

* Added a test suite covering label text generation, configuration resolution, and label rendering, including regression tests for both bug fixes above. The tests need neither a database nor a NetBox installation, and can be run with `python runtests.py` or, inside a NetBox installation, with `./manage.py test netbox_qrcode.tests`.
* Added a CI workflow running the test suite against Python 3.12, 3.13, and 3.14, building the documentation with `mkdocs build --strict`, and verifying that the label templates are present in the built wheel.
* Declared `packaging` as a runtime dependency. It is imported by `template_content.py` but was previously undeclared, so the package was only importable because NetBox happens to depend on it as well.
* Added `test` and `docs` extras, and a `docs/requirements.txt` for building the documentation site.
* Corrected the `Development Status` classifier from Pre-Alpha to Production/Stable, and declared the supported Python versions.
* Documentation restructured into an MkDocs site.
* Added a security policy, issue templates, and a pull request template, and documented the repository's branch model: `feature` for active development of future releases (and the base for pull requests), `main` for released code and the branch releases are cut from.
* Removed the invalid `min_version` and `max_version` arguments from `setup.py`, which setuptools silently discarded. The supported NetBox range is declared in `PluginConfig`, which is where it takes effect.
* Declared `python_requires='>=3.12'` to match NetBox 4.7's supported Python versions.
* Replaced the deprecated `License ::` classifier with an SPDX `license` declaration, and dropped references to bundled `.ttf` font files, which were removed when label rendering moved to CSS.
* Development environment updated for NetBox 4.7: Redis raised to 7 (4.7 requires Redis 6.0 or later).
* Fixed the `relpatch` Makefile target, which referenced a `develop` branch that does not exist in this repository. Releases are now cut from `RELEASE_BRANCH` (defaulting to `main`). Its "git status is not clean" guard never fired, because a `make` conditional is evaluated before the recipe's `$(eval)` runs; it is now a shell test. Added guards for a missing `pysemver` and for an empty computed version, either of which previously produced a branch named `release-` and wrote an empty `__version__`.

---

## Earlier Releases

Releases prior to v1.0.0 predate this change log. See the [GitHub releases page](https://github.com/netbox-community/netbox-qrcode/releases) and the [compatibility matrix](https://github.com/netbox-community/netbox-qrcode/blob/main/COMPATIBILITY.md) for their supported NetBox versions.
