# Usage

## Inspect a project

```bash
patchguide check .
patchguide check /path/to/php-project
patchguide check . --json report.json
patchguide check . --json -
```

## Review local advisory records

```bash
patchguide advisories list
patchguide advisories show CVE-2026-109618
patchguide version
```

## Use in CI

By default, findings are informational and the command exits 0 if the scan completed. Use an explicit policy when you want a CI gate:

```bash
patchguide check . --fail-on affected
patchguide check . --fail-on unknown
```

- `--fail-on never` (default): exit 0 when the scan completes.
- `--fail-on affected`: exit 1 when at least one advisory status is affected.
- `--fail-on unknown`: exit 1 when at least one advisory status is unknown.
- Exit 2 indicates invalid input or unreadable data.

A successful command does not prove a production service is safe. Check that the detected PHP version matches the deployed runtime, and review official vendor guidance for backports. Unknown status should be handled intentionally rather than treated as safe.
