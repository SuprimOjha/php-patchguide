# Changelog

## 0.2.0

- Added mitigation-only advisory records without invented fixed-version claims.
- Added CVE-2026-115560 guidance based on the official PHP session upload progress notice.
- Added static INI discovery for session upload progress and session serialization settings.
- Added report statuses for mitigation required and mitigation configured.
- Added `--fail-on mitigation-required` for CI policy.
- Improved the official archive monitor to compare CVE identifiers with the local database.
- Added regression tests for mitigation evaluation, INI parsing, archive discrepancy reporting, and advisory-copy synchronization.
- Updated documentation and schemas for version-based and mitigation-only records.

This version remains an early-stage security helper. Static configuration and version checks cannot prove the state of every production worker or cover all PHP vulnerabilities.

## 0.1.0

Initial public implementation of PHP PatchGuide.

- Read-only project inspection for Composer metadata, PHP source files, PHP version pins, and Dockerfile PHP image tags.
- Local advisory evaluation with fixed-version comparisons and explicit unknown states.
- Human-readable and JSON reports.
- Opt-in CI failure policies for affected and unknown findings.
- Advisory record validation, a JSON Schema, and upstream references for the bundled PHP security records.
- Tests across Python 3.10–3.13 and a built-wheel smoke test outside the source checkout.
- Scheduled snapshot of the official PHP archive for manual review.
- Documentation covering installation, architecture, limitations, CI integration, security, and advisory review.
