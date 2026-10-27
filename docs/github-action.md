# GitHub Actions integration

PHP PatchGuide includes a composite action in `action.yml`, so a PHP repository can run the scanner without writing its own install and command steps.

## Quick setup

Add this to `.github/workflows/php-security.yml` in the PHP repository:

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

For a reproducible production setup, pin the action to a reviewed release tag or full commit SHA rather than `@main`. Until a versioned action release exists, `@main` is convenient for trying it but can change.

## Inputs

| Input | Default | Meaning |
| --- | --- | --- |
| `path` | `.` | PHP project directory, relative to the workspace |
| `fail-on` | `affected` | `never`, `affected`, `unknown`, or `mitigation-required` |
| `report-path` | `patchguide-report.json` | JSON report path relative to the workspace |

The action sets up Python 3.12 and installs PatchGuide from the action checkout. It does not install PHP or run the PHP application. Findings are based on the local runtime available to the runner, project files, and the bundled advisory data. That runner runtime may not match production.

The report path is also exposed as an action output named `report-path`. If the scan fails because the selected policy is triggered, the scan step fails; put artifact upload behind `if: always()` if you want to preserve the report.

See [limitations](limitations.md) before using the result as a deployment gate.
