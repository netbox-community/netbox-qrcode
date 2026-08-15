# AGENTS.md — netbox-qrcode

## Repository Overview

`netbox-qrcode` is a NetBox plugin that renders printable QR code labels on object detail pages. A label combines a QR code (encoding the object's URL by default) with text drawn from the object's own fields, and its layout is defined entirely in configuration.

The plugin is unusually thin for a NetBox plugin: it has **no models, no migrations, no views, no REST or GraphQL API, and no database access**. It consists of `PluginTemplateExtension` subclasses that render Django templates into the right-hand or left-hand column of existing NetBox detail views. Everything a user can change lives in `PLUGINS_CONFIG`.

Labels are rendered for `dcim.device`, `dcim.module`, `dcim.rack`, `dcim.cable`, `dcim.location`, `dcim.powerfeed` and `dcim.powerpanel`, plus `netbox_inventory.asset` when [netbox-inventory](https://github.com/ArnesSI/netbox-inventory) is installed. The supported NetBox range is in `COMPATIBILITY.md` (4.7.0 – 4.7.x at the time of writing).

## Tech Stack

- Python (defer to `setup.py`; currently `>=3.12`)
- NetBox (host app — minimum and maximum versions are pinned in `netbox_qrcode/__init__.py` `min_version` / `max_version`; `COMPATIBILITY.md` summarises the matrix)
- Django (provided by NetBox — 6.0.x on NetBox 4.7). Used both to render the plugin's own templates and to render user-supplied `text_template` / `url_template` strings
- `qrcode` + `Pillow` — QR image generation, emitted as a base64 PNG data URI
- `packaging` — version comparison in `template_content.py`
- `unittest` (standard library) for tests — **not** pytest, and not `django.test.TestCase`
- mkdocs + mkdocs-material for user-facing docs

There is no linter configured in this repo. Defer all version pins to `setup.py` and `netbox_qrcode/__init__.py`.

## Repository Map

```text
.
├── netbox_qrcode/
│   ├── __init__.py                  — QRCodeConfig (PluginConfig): version pins and default_settings.
│   │                                  default_settings is the single source of truth for every
│   │                                  configuration parameter and its default.
│   ├── template_content.py          — PluginTemplateExtension subclasses, one per supported model.
│   │                                  Holds the per-label loop, error isolation, and config-key naming.
│   ├── template_content_functions.py— Label content helpers: config resolution, URL, text, QR.
│   ├── utilities.py                 — get_qr() / get_img_b64(): qrcode + Pillow wrappers.
│   ├── version.py                   — __version__ (read by setup.py and the relpatch target).
│   ├── templates/netbox_qrcode/
│   │   ├── qrcode3.html             — The label panel. All layout lives here as inline CSS.
│   │   ├── qrcode3_sub_qrcode.html  — The QR image block, {% include %}d by qrcode3.html.
│   │   ├── qrcode_error.html        — Shown in place of a label that failed to render.
│   │   └── qrcode.html              — Legacy NetBox 1/2 panel. Unreachable; see Architecture.
│   └── tests/                       — Standalone unittest suite; needs no database or NetBox.
├── docs/                            — mkdocs site (see mkdocs.yml for nav).
│   ├── index.md, installation.md, configuration.md, label-examples.md, printing.md, changelog.md
│   ├── requirements.txt             — mkdocs-material, for building the docs.
│   └── img/                         — Screenshots referenced by the docs.
├── develop/                         — Docker Compose dev environment, driven by the Makefile.
│   ├── Dockerfile                   — Clones NetBox at NETBOX_VER and pip-installs this plugin -e.
│   ├── docker-compose.yml           — netbox, worker, postgres, redis.
│   ├── configuration.py             — NetBox config for the dev environment, incl. PLUGINS_CONFIG.
│   └── dev.env                      — Dev credentials (not secrets).
├── runtests.py                      — Standalone test runner; stubs netbox.plugins if absent.
├── setup.py                         — Packaging. install_requires, extras (test, docs), classifiers.
├── Makefile                         — Dev environment and release helpers.
├── COMPATIBILITY.md                 — Plugin release to NetBox version matrix.
└── .github/workflows/
    ├── lint-tests.yaml              — docs build, package build, test matrix.
    └── pub-pypi.yml                 — Publishes to PyPI on a published GitHub release.
```

## Architecture

### The label pipeline

For each supported model, `template_content.py` defines a `PluginTemplateExtension` subclass declaring `models = ('dcim.device',)` and implementing `right_page()` or `left_page()`. Both delegate to `Create_PluginContent()`, and the chain is:

```
right_page()
  └─ Create_PluginContent()          — loops label designs 1..10, isolating failures
       └─ Create_SubPluginContent(n)  — renders one label
            ├─ config_for_modul()     — resolves the configuration for this model and label
            ├─ create_url()           — QR payload: object URL, or url_template
            ├─ create_QRCode()        — base64 PNG via get_qr() / get_img_b64()
            ├─ create_text()          — text_fields list, or text_template
            └─ self.render('netbox_qrcode/qrcode3.html', ...)
```

Layout is not computed in Python. Every dimension is passed into `qrcode3.html` as a string (`'56mm'`, `'2.2in'`) and applied as inline CSS, so the browser does the layout and printing is a browser concern. This is why fonts are whatever the printing machine has installed, and why the plugin bundles no font files.

### Configuration resolution

Three layers, each overriding the previous:

1. `QRCodeConfig.default_settings` in `__init__.py`
2. Global keys under `netbox_qrcode` in `PLUGINS_CONFIG`
3. The module-dependent block for the model being viewed (`device`, `rack`, …)

`config_for_modul()` implements this. It copies the config dict before updating it, so resolution never mutates the process-wide `PLUGINS_CONFIG`.

### Configuration key derivation

`model_config_key(models)` maps a template extension's `models` tuple to its configuration key by stripping the app label: `'dcim.device'` → `'device'`, `'netbox_inventory.asset'` → `'asset'`. It splits on the first `.` only, so it works for any app label without special-casing.

Use this helper anywhere a config key is needed. Deriving the key twice in different ways is exactly what caused issue #140, where additional asset labels became unreachable.

### Multiple label designs

A model can have up to ten designs: its base key plus `_2` … `_10`. `Create_PluginContent()` walks them in order and **stops at the first missing number** — `device_2` and `device_4` without `device_3` means `device_4` never renders. This is intentional and documented; do not "fix" it without a docs change.

`Config_Name(n)` returns the key for design *n* (`device`, then `device_2`), and is used for both lookup and error attribution.

### Error isolation

Each label design renders inside its own `try`/`except` in `Create_PluginContent()`. A design that raises is logged as a warning to `netbox.plugins.netbox_qrcode` and replaced with `qrcode_error.html`, naming the configuration key at fault; the object's other labels still render.

This matters because NetBox core wraps every template extension call in a broad `except` (`netbox/utilities/templatetags/plugins.py`) and substitutes its own error template. Anything escaping `right_page()` therefore costs *all* of the plugin's output, not just the failing label — that was issue #141. Keep the per-label boundary intact when changing this loop.

### The `qr_` prefix convention

`create_QRCode()` sweeps the resolved config for keys starting with `qr_`, strips the prefix, and passes the rest as keyword arguments to `qrcode.QRCode()`:

```python
'qr_box_size': 4   →   qrcode.QRCode(box_size=4)
```

So adding a `qr_*` parameter needs no plumbing — but it also means a typo like `qr_bogus` reaches `QRCode()` and raises `TypeError`. Two open PRs (#112, #129) extend this area; both change `get_qr()` and conflict with each other.

### The legacy template

`Create_SubPluginContent()` gates on `version.parse(settings.RELEASE.version).major >= 3` and falls back to `qrcode.html` for NetBox 1/2. Since `min_version` is `4.7.0` this branch is unreachable, and `qrcode.html` and the `packaging` import exist only to serve it. Removing all three is a known cleanup, deliberately not yet done.

### Key files

| File | Why you'd open it |
|---|---|
| `netbox_qrcode/__init__.py` | Add or change a configuration parameter or its default; bump the NetBox version range |
| `netbox_qrcode/template_content.py` | Add support for a new model; change the per-label loop or error handling |
| `netbox_qrcode/template_content_functions.py` | Change how text, URLs, or configuration are resolved |
| `netbox_qrcode/utilities.py` | Change QR image generation |
| `netbox_qrcode/templates/netbox_qrcode/qrcode3.html` | Change label layout or the panel chrome |
| `docs/configuration.md` | Document a parameter — required for any new one |

## Commands

| Command | What it does |
|---|---|
| `python runtests.py` | Run the full test suite. No database, NetBox, or Redis needed |
| `python runtests.py -v` | Same, verbose |
| `make cbuild` | Build the dev environment images |
| `make debug` | Start the dev environment in the foreground (NetBox on `:8000`) |
| `make start` / `make stop` | Start detached / tear down |
| `make destroy` | Tear down and delete the Postgres volume |
| `make adduser` | Create a NetBox superuser |
| `make nbshell` / `make shell` | NetBox shell / Django shell in the container |
| `pip install -r docs/requirements.txt` | Install the docs toolchain |
| `mkdocs serve` | Preview the docs |
| `mkdocs build --strict` | Build the docs; fails on broken internal links (CI runs this) |
| `python -m build` | Build sdist + wheel |
| `make relpatch` | Bump the patch version and push a release branch (needs `pip install semver`) |

## Development

Two ways to work, depending on what you're changing.

**Logic changes — use `runtests.py`.** Label generation is pure Python plus Django template rendering, so the suite runs in under a second with no services. `runtests.py` supplies what NetBox normally would: it stubs `netbox.plugins` when NetBox is not importable, and configures Django with the plugin's template directory. This is the fast loop and what CI uses.

**Anything visual — use the dev environment.** Layout, printing, and panel chrome need a real browser against real objects:

```
make cbuild
make debug
make adduser     # in another shell
```

NetBox comes up on `http://localhost:8000`. `develop/docker-compose.yml` mounts `netbox_qrcode/` into the container, so Python changes take effect on reload; `develop/configuration.py` holds the dev `PLUGINS_CONFIG` and is the place to try label designs.

`NETBOX_VER` and `PYTHON_VER` at the top of the `Makefile` control what NetBox is built against. `NETBOX_VER` is a git ref of the NetBox repo, so it can be a branch (`feature`, `main`) or a tag (`v4.7.0`) — during a pre-release cycle it will be a branch, because no tag exists yet.

There are no migrations to generate: this plugin has no models.

## Testing

- Tests use plain `unittest`, **not** pytest and **not** `django.test.TestCase`. They live in `netbox_qrcode/tests/`.
- Run with `python runtests.py` from the repository root. Inside a NetBox installation, `./manage.py test netbox_qrcode.tests` also works — the tests ship in the wheel for exactly this reason.
- The suite deliberately needs no database. Do not introduce a test that requires one without a good reason; it would force Postgres into CI for a plugin that never touches a database.
- NetBox models are not imported. `tests/base.py` provides stand-ins (`FakeDevice`, `FakeCable`, `FakeInterface`, `FakeAsset`, `FakeRequest`) which define `__repr__` in the same shape Django models use (`<ClassName: str(self)>`). That detail matters: issue #139 was a Python `repr` leaking onto labels, and a stand-in without `__repr__` would not reproduce it.

| Module | Coverage area |
|---|---|
| `test_text_content.py` | `get_text_fields`, `create_text`, text templates, multi-value fields (#139) |
| `test_configuration.py` | `model_config_key`, config-key agreement (#140), three-layer resolution |
| `test_rendering.py` | QR generation, `create_url`, full label render, multiple designs |
| `test_error_isolation.py` | Per-label error isolation, attribution, logging, escaping (#141) |
| `base.py` | Shared stand-in objects and config helpers |

When fixing a bug, add a regression test that fails before the fix. The three fixed issues above each have one, and they are the reason the suite exists.

## CI/CD

GitHub Actions in `.github/workflows/`:

- **`lint-tests.yaml`** — runs on pull requests and on pushes to `main` / `feature`. Three jobs:
  - *docs* — installs `docs/requirements.txt` and runs `mkdocs build --strict`, so a broken internal link fails the build.
  - *package* — `python -m build`, `twine check`, then asserts the label templates are present in the built wheel. Adding a template means adding it to that list, or it ships unverified.
  - *tests* — `python runtests.py -v` on Python 3.12, 3.13 and 3.14. No services.
- **`pub-pypi.yml`** — runs on a published GitHub release; builds and uploads to PyPI using an API token.

Actions in `lint-tests.yaml` are SHA-pinned. `pub-pypi.yml` still uses floating refs and token auth; modernising it is a known cleanup.

## Common Tasks

### Add a configuration parameter

1. Add it to `default_settings` in `netbox_qrcode/__init__.py`. This is the source of truth.
2. If it is a `qr_*` parameter it reaches `qrcode.QRCode()` automatically. Otherwise thread it into the `extra_context` dict in `Create_SubPluginContent()` and use it in `qrcode3.html`.
3. Document it in `docs/configuration.md` with a `Default:` line, in the section it belongs to.
4. Add a test.
5. Add a changelog entry.

### Add support for a new model

1. Subclass `QRCode` in `template_content.py` with `models = ('<app_label>.<model>',)` and implement `right_page()` or `left_page()` returning `self.Create_PluginContent()`.
2. Append it to `template_extensions`. If the model comes from another plugin, guard the append on that plugin being importable — see `INVENTORY_AVAILABLE`.
3. Add a default block keyed by the model name to `default_settings` (even an empty dict).
4. Add the class to `EXTENSIONS` in `tests/test_configuration.py`, which asserts every extension's config key resolves.
5. Document the key in `docs/configuration.md` and update the supported-types list in `README.md` and `docs/index.md`.

### Bump the supported NetBox version

1. Update `min_version` / `max_version` in `netbox_qrcode/__init__.py`.
2. Add a row to `COMPATIBILITY.md`.
3. Update `NETBOX_VER` in the `Makefile` if the dev environment should track a new ref.
4. Check the new NetBox release notes for changes to `PluginTemplateExtension`, the template extension context, or anything the plugin relies on (`settings.RELEASE`, `get_absolute_url`, Django's version).
5. Bump the Django pin in the `test` extra in `setup.py` if NetBox moved to a new Django series.

### Cut a release

`make relpatch` bumps the patch version in `version.py` and pushes a `release-<version>` branch from `RELEASE_BRANCH`. It guards on a clean tree, `pysemver` being installed, and a non-empty computed version. Publishing to PyPI happens when a GitHub release is published.

## Conventions and Patterns

- **Branches.** `feature` is active development and the base for pull requests. `main` is released code and what releases are cut from. GitHub defaults new PRs to `main`, so the base usually needs changing.
- **Existing naming is unusual — match it.** Methods on the template extension classes are `PascalCase_WithUnderscores` (`Create_PluginContent`, `Config_Name`) and module functions are `snake_case` (`create_url`, `model_config_key`). This is not PEP 8, but consistency within the file wins over correcting it.
- **Comment style.** Functions carry a `####` banner with a short description and a `# Parameter:` block. Keep it.
- **Dimensions are strings with units**, never numbers: `'12mm'`, `'0.47in'`. They pass straight into CSS.
- **Never mutate the config dict** you were given. `PLUGINS_CONFIG` is process-wide and shared across requests; copy before updating.
- **Nothing user-supplied should be trusted as HTML** except where that is the documented feature. `text_template` intentionally allows HTML; the error panel escapes the exception text because it embeds configuration values.
- **A new configuration parameter is not done until it is in `docs/configuration.md`.** The docs are the reference; `default_settings` is not user-facing.
- **Changelog.** User-visible changes get an entry in `docs/changelog.md` under the current version, with the issue link.

## Troubleshooting

**No label panel appears at all.** Check the plugin loaded: a NetBox version outside `min_version`/`max_version` raises `IncompatiblePluginError` at startup. Then check the model is one the plugin registers.

**The panel shows "configuration error".** One label design failed. The panel names the config key; the full exception is logged as a warning to `netbox.plugins.netbox_qrcode`. The most common cause is a misspelled `qr_*` key reaching `qrcode.QRCode()`.

**An additional label design is ignored.** The numbering must be contiguous. `device_2` and `device_4` without `device_3` stops the chain at 2.

**`TemplateDoesNotExist`.** The templates are package data. Confirm they are in the installed wheel — the `package` CI job asserts this.

**A printed QR code will not scan.** Usually the quiet zone: `qr_border` defaults to `0`. Raise it, and raise `qr_error_correction`, when the code is small or printed on a textured label. See `docs/printing.md`.

**The label looks right on screen but prints wrong.** Almost always browser print scaling. See `docs/printing.md`.

## References

- User documentation: `docs/` (built with mkdocs; `mkdocs.yml` has the nav)
- Supported NetBox versions: `COMPATIBILITY.md`
- [NetBox plugin development docs](https://netboxlabs.com/docs/netbox/plugins/development/)
- [`PluginTemplateExtension` source](https://github.com/netbox-community/netbox/blob/main/netbox/netbox/plugins/templates.py) — the context keys and available methods
- [How NetBox renders template extensions](https://github.com/netbox-community/netbox/blob/main/netbox/utilities/templatetags/plugins.py) — relevant to error handling
- [qrcode](https://pypi.org/project/qrcode/) — the `qr_*` parameters map to `qrcode.QRCode()`
