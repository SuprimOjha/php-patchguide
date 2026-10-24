# CI integration

Use patchguide check . --json patchguide-report.json. The CLI does not fail solely because findings exist. Before enforcing a CI gate, confirm the version represents the deployed runtime, decide how unknown results should be handled, and review vendor backports. Parse the report and define your own policy.
