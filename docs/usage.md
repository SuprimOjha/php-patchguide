# Usage

- patchguide check . inspects the current project.
- patchguide check . --json report.json writes a JSON report.
- patchguide check . --json - emits JSON to stdout.
- patchguide advisories list lists local records.
- patchguide advisories show CVE-2026-109618 displays one record.
- patchguide version prints the tool version.

Exit code 0 means the command completed; findings are informational. Exit code 2 indicates invalid input or unreadable data. The CLI does not execute application files.
