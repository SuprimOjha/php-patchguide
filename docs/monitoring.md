# Scheduled monitoring

The weekly GitHub Actions job fetches the current year's official PHP archive and uploads a JSON snapshot artifact. It extracts CVE identifiers, compares them with local advisory IDs, and records possible gaps in both directions.

When the archive contains a CVE identifier missing from the local database, the script prints a review warning to stderr. It does **not** automatically trust the identifier, create a record, update fixed versions, or commit changes. Maintainers should open the official notice, verify severity/affected versions/mitigations, update both source and packaged records, and add regression tests.

The monitor is a review aid, not a guarantee of comprehensive coverage. Changes to the PHP archive markup may require maintenance. Review the artifact and [advisory conventions](advisory-conventions.md) regularly.
