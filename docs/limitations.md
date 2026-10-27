# Limitations

PatchGuide is an early-stage security helper, not a comprehensive vulnerability scanner.

- **Runtime mismatch:** local CLI PHP may differ from PHP-FPM, Apache/mod_php, containers, or production hosting.
- **Static configuration:** INI files in the repository may not be loaded by the active service. A setting detected as disabled in one file does not prove every worker uses it.
- **Application behavior:** the scanner does not prove whether code changes `session.serialize_handler` at runtime before `session_start()`.
- **Version checks:** vendor distributions may backport fixes without changing the upstream version string.
- **Limited database:** local records are reviewed manually and are not exhaustive. Archive monitoring flags potential new CVE identifiers but does not automatically ingest them.
- **No dependency audit:** it does not replace Composer package auditing, source analysis, web-server configuration review, or penetration testing.
- **No auto-remediation:** it does not edit project files, restart services, or deploy patches.

Treat unknown as unknown, not as safe. Verify official PHP and vendor advisories before making production decisions.
