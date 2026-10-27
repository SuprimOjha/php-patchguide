# Advisory data

One JSON file per CVE. Records currently use two types:

- `kind: "version"` (or omitted): compare the detected PHP version with a reviewed `fixed_by` mapping.
- `kind: "mitigation"`: provide mitigation guidance when no fixed version is confirmed. These records must not claim a fixed version.

The critical CVE-2026-109618 and CVE-2026-109619 records reference the PHP security release announcement dated 21 October 2026. The official archive lists fixed releases 8.5.12, 8.4.27, 8.3.36, and 8.2.35: https://www.php.net/archive/2026.php

CVE-2026-115560 tracks the PHP team's 23 October 2026 session upload progress notice: https://www.php.net/archive/2026.php#2026-10-23-1. It has no fixed-version claim; the recommended setting is `session.upload_progress.enabled=0` until the next regular bug-fix release.

Keep `advisories/` and `src/patchguide/data/advisories/` synchronized. Validate changes against `advisories/schema.json`, review upstream sources, and add tests for new evaluation behavior. Version and static-configuration checks are evidence, not proof of production runtime status.
