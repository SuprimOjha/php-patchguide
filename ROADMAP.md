# Roadmap

This is a practical list of improvements, not a promise that every item will ship on a particular date.

## Current focus

- [x] Read-only project discovery and local CLI version detection.
- [x] Local, reviewable JSON advisory records.
- [x] Human-readable and JSON output.
- [x] CI exit policies and a reusable GitHub Action.
- [x] Tests for supported Python versions, installed-wheel behavior, and the composite GitHub Action.
- [x] Scheduled snapshot of the official PHP archive for manual review.

## Next

- [ ] Expand the advisory database only with official sources, affected ranges, and reviewed remediation guidance.
- [ ] Improve PHP runtime/configuration discovery for common Docker Compose and CI layouts.
- [ ] Add a machine-readable rule to each finding explaining exactly which evidence triggered it.
- [x] Add a regression test so conflicting INI values produce an unknown result instead of a misleading mitigation claim.
- [ ] Improve detection of actual PHP INI configuration precedence across runtime, pool, and directory settings.
- [ ] Publish versioned releases and pin the GitHub Action to release tags.
- [ ] Collect anonymized, opt-in feedback about false positives without uploading project files by default.
- [ ] Add a compact Markdown report for pull-request comments, if it can be done without introducing noisy findings.

## Out of scope for now

- Claiming that a repository scan proves a production service is secure.
- Automatically editing configuration or upgrading PHP on a user's behalf.
- Automatically trusting newly discovered CVE IDs without reviewing the upstream advisory.
- Adding a large dependency solely for a small feature.

## How to help

Check the issue tracker before starting large changes. A good contribution includes a minimal reproducer or fixture, a test, and a link to the upstream source when it changes security advice.
