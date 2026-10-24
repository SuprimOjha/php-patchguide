# PHP PatchGuide

[![Tests](https://github.com/SuprimOjha/php-patchguide/actions/workflows/tests.yml/badge.svg)](https://github.com/SuprimOjha/php-patchguide/actions/workflows/tests.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

A read-only PHP security helper with project detection, a local advisory database, text/JSON reports, CI exit policies, tests, and GitHub Actions.

## Quick start

Requires Python 3.10+.

```bash
git clone https://github.com/SuprimOjha/php-patchguide.git
cd php-patchguide
python -m pip install -e .
patchguide check .
patchguide advisories list
patchguide advisories show CVE-2026-109618
patchguide check . --json report.json
```

Run the test suite:

```bash
python -m unittest discover -s tests -v
```

## Features

- Inspects Composer metadata, PHP file names, Dockerfile PHP image tags, and version pins.
- Detects the local CLI PHP version using `php -v`, with a timeout.
- Compares the detected version with reviewed local advisory records.
- Produces human-readable and JSON reports.
- Offers opt-in CI exit policies for known affected or unknown results.
- Includes a JSON schema for advisory records and a wheel-install smoke test in CI.
- Local checks do not modify project files, execute application PHP, or send project data over the network.

## CI usage

```bash
patchguide check . --json patchguide-report.json --fail-on affected
```

Exit policy:

- `--fail-on never` (default): return success if the scan completes.
- `--fail-on affected`: exit 1 if any known advisory marks the detected version affected.
- `--fail-on unknown`: exit 1 if any advisory status is unknown.
- Exit 2 indicates invalid input or unreadable data.

See [CI integration](docs/ci-integration.md) before using a security gate.

## Important limitations

PatchGuide is an early-stage helper, **not a complete vulnerability scanner**. The CLI PHP version can differ from PHP-FPM, Apache/mod_php, containers, and managed hosting. Composer constraints are not proof of the deployed runtime. Version-only checks cannot reliably identify vendor backports. The local advisory database is intentionally limited and is not fetched or updated during a scan.

The bundled records cover two critical PHP issues announced on 21 October 2026. The official PHP archive lists patched releases 8.5.12, 8.4.27, 8.3.36, and 8.2.35. Read the upstream advisories before taking action: [CVE-2026-109618](https://github.com/php/php-src/security/advisories/GHSA-w8hw-w9fx-j79w), [CVE-2026-109619](https://github.com/php/php-src/security/advisories/GHSA-6wmf-4rv5-p3rp), [PHP security archive](https://www.php.net/archive/2026.php), and [supported versions](https://www.php.net/supported-versions.php).

## Documentation

- [Installation and usage](docs/usage.md)
- [Architecture](docs/architecture.md)
- [Limitations](docs/limitations.md)
- [CI integration](docs/ci-integration.md)
- [Advisory data conventions](docs/advisory-conventions.md)
- [Security policy](SECURITY.md)
- [Contributing](CONTRIBUTING.md)
- [Changelog](CHANGELOG.md)

## License

MIT. See [LICENSE](LICENSE).
