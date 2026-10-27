# CI integration

Install PatchGuide in the CI environment and run:

```bash
python -m pip install .
patchguide check . --json patchguide-report.json --fail-on affected
```

For strict handling of unknown evidence:

```bash
patchguide check . --json patchguide-report.json --fail-on unknown
```

To fail when a mitigation-only advisory detects a configuration needing attention:

```bash
patchguide check . --json patchguide-report.json --fail-on mitigation-required
```

The policy controls the exit code; it does not change the findings. Version policies apply only to the detected CLI version and local records. The mitigation policy is based on static INI evidence; it cannot prove effective settings in PHP-FPM, Apache, containers, or every worker.

Keep JSON reports as CI artifacts only if workspace paths are acceptable to disclose. Review official vendor advisories for backports before enforcing gates, and decide how your team handles unknown results.
