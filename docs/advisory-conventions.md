# Advisory data conventions

PatchGuide stores reviewed advisory records as JSON in `advisories/`. The installable wheel includes copies under `src/patchguide/data/advisories/`; keep those copies synchronized when changing records.

## Required fields

- `id`: CVE identifier.
- `title`: concise upstream title.
- `severity`: upstream severity, represented as a string.
- `fixed_by`: mapping from PHP branch (for example `8.4`) to the first fixed patch release.
- `url`: canonical upstream advisory URL.

Useful additional fields include `published`, `summary`, `affected`, `references`, `weaknesses`, and `notes`. Validate new or edited records against [schema.json](../advisories/schema.json).

## Review requirements

1. Prefer official PHP security advisories and release announcements.
2. Record the patched version separately for each supported branch; do not infer that a fix on one branch implies the same patch number on another.
3. Keep summaries concise and faithful to upstream wording. Link to upstream details rather than copying long advisory text.
4. Never treat version comparison as proof that a vendor build is vulnerable or safe. Vendors may backport patches without changing the upstream version string.
5. Do not add a record based solely on an unverified social post, issue comment, or speculative report.
6. Keep the source and packaged JSON copies synchronized.
7. Add tests for fixed-version comparison, unknown branches, malformed records, and any changed evaluation behavior.

The runtime check validates the minimum structure needed to make a comparison; it is not a replacement for full JSON Schema validation or human review.
