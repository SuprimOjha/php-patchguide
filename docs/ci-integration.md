# CI integration

Install PatchGuide in the CI environment and run:

```bash
python -m pip install .
patchguide check . --json patchguide-report.json --fail-on affected
```

For strict handling of unknown results:

```bash
patchguide check . --json patchguide-report.json --fail-on unknown
```

The `--fail-on` policy controls the exit code; it does not change the findings. Use `affected` to fail only when a known local advisory marks the detected CLI version affected. Use `unknown` if missing runtime evidence or missing fix rules should block the pipeline. These policies do not prove the version represents PHP-FPM, Apache, a container, or production hosting.

Review vendor advisories for backports before enforcing a gate. Keep the JSON report as a CI artifact for audit and troubleshooting. Avoid uploading reports if project paths are sensitive; report paths may reveal workspace layout.
