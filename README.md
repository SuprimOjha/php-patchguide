# PHP PatchGuide

A read-only PHP security helper with project detection, local advisory checks, text/JSON reports, tests, and GitHub Actions.

## Quick start

Requires Python 3.10+.

    git clone https://github.com/SuprimOjha/php-patchguide.git
    cd php-patchguide
    python -m pip install -e .
    patchguide check .
    patchguide advisories list
    patchguide advisories show CVE-2026-109618
    patchguide check . --json report.json

Run tests with: python -m unittest discover -s tests -v

## What it does

- Reads Composer metadata, PHP source file names, Dockerfile PHP image tags, and version pins.
- Detects the local CLI PHP version without executing application code.
- Compares that version with reviewed local advisory records.
- Emits JSON for CI workflows.
- Does not modify projects, upgrade packages, deploy code, or upload local project data.

Important: the CLI version may differ from PHP-FPM, Apache/mod_php, containers, or managed hosting. Version-only checks cannot reliably identify vendor backports. Verify findings with official PHP and vendor security notices.

The initial records cover the two critical issues announced on 21 October 2026. PHP's official archive lists fixed releases 8.5.12, 8.4.27, 8.3.36, and 8.2.35: https://www.php.net/archive/2026.php and https://www.php.net/supported-versions.php.

## Commands

- patchguide check PATH: inspect a project and evaluate known advisories.
- patchguide check PATH --json FILE: write a JSON report.
- patchguide check PATH --json -: emit JSON to standard output.
- patchguide advisories list: list local records.
- patchguide advisories show CVE-ID: display one record.
- patchguide version: print the tool version.

See docs/ for installation, usage, architecture, limitations, advisory review, and operational checklists. Read CONTRIBUTING.md and SECURITY.md before contributing.

License: MIT.
