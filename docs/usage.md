# Usage

## Inspect a project

```bash
patchguide check .
patchguide check /path/to/php-project
patchguide check . --json report.json
patchguide check . --json -
```

The scan is read-only. It inspects project metadata, selected PHP file/configuration names, Dockerfile PHP image tags, version pins, and the local CLI runtime. It does not execute application PHP.

## Review local advisory records

```bash
patchguide advisories list
patchguide advisories show CVE-2026-109618
patchguide advisories show CVE-2026-115560
patchguide version
```

## Use in CI

```bash
patchguide check . --json report.json --fail-on affected
patchguide check . --json report.json --fail-on mitigation-required
```

- `--fail-on never` (default): exit 0 when the scan completes.
- `--fail-on affected`: exit 1 when a version-based advisory marks the detected CLI version affected.
- `--fail-on unknown`: exit 1 when at least one finding is unknown.
- `--fail-on mitigation-required`: exit 1 when a mitigation-only record identifies a required mitigation from scanned configuration.
- Exit 2 indicates invalid input or unreadable data.

## Session upload progress mitigation

For CVE-2026-115560, PHP recommends `session.upload_progress.enabled=0` until the next regular bug-fix release. PatchGuide looks for explicit values in discovered INI files and reports `mitigation_required`, `mitigated`, or `unknown`. A disabled value in one file is not proof every serving worker uses it. Review [the official PHP notice](https://www.php.net/archive/2026.php#2026-10-23-1), check the effective configuration, and restart serving workers as directed by your operations process.

A successful scan does not prove a production service is safe. Unknown status is not equivalent to fixed.
