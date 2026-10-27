# PHP PatchGuide

[![Tests](https://github.com/SuprimOjha/php-patchguide/actions/workflows/tests.yml/badge.svg)](https://github.com/SuprimOjha/php-patchguide/actions/workflows/tests.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python versions](https://img.shields.io/badge/python-3.10%E2%80%933.13-blue)](https://www.python.org/downloads/)

PHP PatchGuide is a small command-line tool for checking a PHP project's local runtime details against a set of reviewed PHP security advisories. It can also look for a few relevant settings in INI files and write a report you can keep with a CI run.

It is deliberately narrow. It does not try to replace a dependency scanner or claim that a production server is secure.

## Install

Python 3.10 or newer is required.

```bash
git clone https://github.com/SuprimOjha/php-patchguide.git
cd php-patchguide
python -m pip install -e .
```

Run it from the root of a PHP project:

```bash
patchguide check .
patchguide advisories list
patchguide advisories show CVE-2026-109618
patchguide check . --json report.json
```

Use `--json -` to print the JSON report to stdout. To run the tests from a checkout:

```bash
python -m unittest discover -s tests -v
```

## What it checks

- Composer's declared PHP requirement and platform version, shown in the human-readable report.
- PHP files, version-pin files, and PHP image tags in Dockerfiles, also shown in the report.
- The version reported by the local `php -v` command.
- Local advisory records with known fixed versions.
- A small set of PHP INI settings, including `session.upload_progress.enabled`; conflicting values are reported as unknown rather than treated as safely configured.

The scan is read-only. It doesn't run your application code or upload project files. The scheduled archive check is separate: it fetches the public PHP archive and creates a snapshot for manual review.

## CI exit codes

For example:

```bash
patchguide check . --json patchguide-report.json --fail-on affected
```

- `--fail-on never` is the default and reports findings without failing for their status.
- `--fail-on affected` returns 1 when a version rule marks a finding as affected.
- `--fail-on unknown` returns 1 when a finding has unknown status.
- `--fail-on mitigation-required` returns 1 when the scanned configuration indicates a mitigation is needed.
- Exit code 2 means the command couldn't complete because of invalid input or an input/read error.

See [CI integration](docs/ci-integration.md) before using a result to block a deployment.

## Use it in GitHub Actions

You can run PatchGuide on pull requests with the composite action included in this repository:

```yaml
name: PHP security check

on:
  pull_request:
  push:
    branches: [main]

permissions:
  contents: read

jobs:
  patchguide:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: SuprimOjha/php-patchguide@main
        with:
          path: .
          fail-on: affected
          report-path: patchguide-report.json
      - if: always()
        uses: actions/upload-artifact@v4
        with:
          name: php-patchguide-report
          path: patchguide-report.json
          if-no-files-found: ignore
```

For a production workflow, pin the action to a reviewed release tag or commit SHA rather than `@main`. The action installs Python and PatchGuide; it does not install PHP or run your application. See [the full action guide](docs/github-action.md).

## Advisory data

The bundled records cover two PHP security advisories with fixed-version information and a separate mitigation note for CVE-2026-115560. For that mitigation-only record, the PHP team's [23 October notice](https://www.php.net/archive/2026.php#2026-10-23-1) recommends setting `session.upload_progress.enabled=0` until a regular bug-fix release addresses the issue. PatchGuide does not assign a fixed version where the notice doesn't provide one.

Sources for the other bundled records: [GHSA-w8hw-w9fx-j79w](https://github.com/php/php-src/security/advisories/GHSA-w8hw-w9fx-j79w), [GHSA-6wmf-4rv5-p3rp](https://github.com/php/php-src/security/advisories/GHSA-6wmf-4rv5-p3rp), and the [PHP release archive](https://www.php.net/archive/2026.php).

The database is small and maintained manually. The archive monitor can flag CVE identifiers that may be missing locally, but it doesn't automatically turn an announcement into a trusted advisory.

## Things to keep in mind

The local CLI version might not match PHP-FPM, Apache, a container, or the server that handles real traffic. An INI file in the repository might not be loaded by that server. Vendor packages can also backport fixes without changing the upstream version string.

For those reasons, a `fixed` result only means the detected version is at or above the fix recorded in this project's data. It is not proof that production is patched. Check the official PHP or vendor notice before acting on a finding.

More detail: [limitations](docs/limitations.md), [runtime notes](docs/php-runtime-map.md), [advisory conventions](docs/advisory-conventions.md), and [security policy](SECURITY.md).

## License

MIT. See [LICENSE](LICENSE).
