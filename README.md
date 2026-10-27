# PHP PatchGuide

[![Tests](https://github.com/SuprimOjha/php-patchguide/actions/workflows/tests.yml/badge.svg)](https://github.com/SuprimOjha/php-patchguide/actions/workflows/tests.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

A read-only PHP security helper that inspects project metadata, compares the local CLI runtime against a reviewed advisory database, checks selected INI settings, and produces text/JSON reports for developers and CI.

## Quick start

Requires Python 3.10+.

```bash
git clone https://github.com/SuprimOjha/php-patchguide.git
cd php-patchguide
python -m pip install -e .
patchguide check .
patchguide advisories list
patchguide advisories show CVE-2026-109618
patchguide advisories show CVE-2026-115560
patchguide check . --json report.json
```

Run all tests:

```bash
python -m unittest discover -s tests -v
```

## Features

- Discovers Composer metadata, PHP files, Dockerfile PHP image tags, and version pins.
- Detects local CLI PHP version with a timeout.
- Checks bundled PHP security records against the detected version.
- Inspects visible INI files for `session.upload_progress.enabled` and related session settings.
- Distinguishes fixed/affected version findings from mitigation-only guidance.
- Produces text and JSON reports, with CI failure policies for affected, unknown, or mitigation-required results.
- Runs tests on Python 3.10–3.13 and smoke-tests the built wheel.
- Scheduled archive monitoring flags CVE identifiers seen upstream but absent from the local database.

## CI usage

```bash
patchguide check . --json patchguide-report.json --fail-on affected
patchguide check . --json patchguide-report.json --fail-on mitigation-required
```

- `--fail-on never`: report only; exit 0 if the scan completed.
- `--fail-on affected`: exit 1 when a known version rule says affected.
- `--fail-on unknown`: exit 1 if any result is unknown.
- `--fail-on mitigation-required`: exit 1 if a reviewed advisory says a mitigation is required based on the discovered config.
- Exit 2 indicates invalid input or unreadable data.

See [CI integration](docs/ci-integration.md) before using a security gate.

## Current advisory coverage

The local database includes two critical PHP issues fixed in PHP 8.5.12, 8.4.27, 8.3.36, and 8.2.35, plus mitigation guidance for CVE-2026-115560. The PHP Security Team recommends setting `session.upload_progress.enabled=0` until the next regular bug-fix release for the unusual configuration/application vector described in its [23 October notice](https://www.php.net/archive/2026.php#2026-10-23-1). This record deliberately has **no fixed version**.

For the critical issues, read [CVE-2026-109618](https://github.com/php/php-src/security/advisories/GHSA-w8hw-w9fx-j79w), [CVE-2026-109619](https://github.com/php/php-src/security/advisories/GHSA-6wmf-4rv5-p3rp), and the [official PHP archive](https://www.php.net/archive/2026.php). The archive monitor identifies possible gaps; it does not automatically trust or ingest new records.

## Important limitations

PatchGuide is an early-stage helper, **not a complete vulnerability scanner**. The CLI version may differ from PHP-FPM, Apache, containers, or production hosting. Static INI files do not prove the effective configuration of every worker. The scan does not prove whether application code changes the session handler dynamically, audit Composer packages, inspect every source-level vulnerability, or account for vendor backports. Local checks do not modify project files, execute application PHP, or send project data over the network.

Always verify findings against official PHP and vendor guidance. See [limitations](docs/limitations.md), [advisory conventions](docs/advisory-conventions.md), [monitoring](docs/monitoring.md), and [security policy](SECURITY.md).

## License

MIT. See [LICENSE](LICENSE).
