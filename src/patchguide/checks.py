"""Compare PHP versions and report mitigation-only advisory guidance."""
from patchguide.versions import compare_versions, parse_version


def evaluate_advisories(version, advisories, ini_settings=None):
    parsed = parse_version(version or "")
    settings = ini_settings or {}
    upload_values = [str(item.get("value", "")).lower()
                     for item in settings.get("session.upload_progress.enabled", [])]
    upload_disabled = bool(upload_values) and upload_values[-1] in {"0", "off", "false", "no"}
    findings = []
    for item in advisories:
        if item.get("kind") == "mitigation":
            enabled = {"1", "on", "true", "yes"}
            disabled = {"0", "off", "false", "no"}
            observed = {value for value in upload_values if value in enabled | disabled}
            if observed & enabled and observed & disabled:
                status = "unknown"
                message = (
                    "Scanned INI files disagree about session.upload_progress.enabled. "
                    "Resolve the conflict and verify the effective value in every serving worker."
                )
            elif observed and observed <= disabled:
                status = "mitigated"
                message = (
                    "All discovered values disable session upload progress; verify the effective "
                    "setting in every serving worker."
                )
            elif observed and observed <= enabled:
                status = "mitigation_required"
                message = (
                    "A discovered INI file enables session upload progress. Set "
                    "session.upload_progress.enabled=0 and verify the effective value in every "
                    "serving worker until the official fix is released."
                )
            else:
                status = "unknown"
                message = (
                    "No explicit usable setting was found in scanned INI files. Set "
                    "session.upload_progress.enabled=0 and verify effective runtime configuration "
                    "until the official fix is released."
                )
            findings.append({"id": item.get("id"), "title": item.get("title"),
                             "severity": item.get("severity", "unknown"), "status": status,
                             "current_version": version, "fixed_version": None,
                             "message": message, "url": item.get("url"),
                             "kind": "mitigation"})
            continue
        fixed = None
        if parsed is None:
            status, message = "unknown", "PHP version not detected; verify serving runtime."
        else:
            series = "{}.{}".format(parsed[0], parsed[1])
            fixed = item.get("fixed_by", {}).get(series)
            if not fixed:
                status, message = "unknown", "No fixed-version rule for PHP {}.".format(series)
            elif compare_versions(version, fixed) == -1:
                status, message = "affected", "Update to {} or later, or verify vendor backports.".format(fixed)
            else:
                status, message = "fixed", "Version is at or above recorded fix {}.".format(fixed)
        findings.append({"id": item.get("id"), "title": item.get("title"),
                         "severity": item.get("severity", "unknown"), "status": status,
                         "current_version": version, "fixed_version": fixed,
                         "message": message, "url": item.get("url"),
                         "kind": item.get("kind", "version")})
    return findings
