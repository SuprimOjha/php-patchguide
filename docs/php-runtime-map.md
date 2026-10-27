# PHP runtime map

A host may have different versions and configuration for CLI, Composer, PHP-FPM, Apache/mod_php, CGI, containers, workers, staging, and production.

PatchGuide detects only the local CLI version and common Dockerfile tags. It reads INI files found in the project tree, but it cannot prove which files are loaded by the active runtime, whether environment overrides apply, or whether every worker has restarted.

For a security check, verify the version and effective configuration in every serving environment directly. For CVE-2026-115560, follow the [official PHP notice](https://www.php.net/archive/2026.php#2026-10-23-1) and confirm `session.upload_progress.enabled=0` is effective in the actual serving workers until the recommended release is available.
