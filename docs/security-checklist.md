# PHP security patch checklist

- [ ] Confirm the PHP version serving production requests.
- [ ] Check PHP-FPM, Apache, CGI, containers, and managed hosting separately.
- [ ] Read official PHP and vendor security notices.
- [ ] Confirm the fix is present in the selected build, including vendor backports.
- [ ] For CVE-2026-115560, set `session.upload_progress.enabled=0` and verify the effective setting in all serving workers until the official PHP notice says the mitigation is no longer needed.
- [ ] Back up and test in staging.
- [ ] Check extension and framework compatibility.
- [ ] Deploy with a rollback plan.
- [ ] Restart services when required and verify runtime, logs, and health checks.
- [ ] Record the change and the source used to verify it.

Official archive: https://www.php.net/archive/2026.php
