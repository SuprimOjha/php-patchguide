# Changelog

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

This release does not claim comprehensive vulnerability coverage. Consult the README and limitations documentation before relying on results in production.
