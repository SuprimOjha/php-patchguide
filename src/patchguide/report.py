"""Human-readable and JSON report formatting."""
import json


def build_report(project, findings):
    states = [item["status"] for item in findings]
    return {
        "tool": "PHP PatchGuide",
        "schema_version": "1.1",
        "project": project,
        "summary": {
            "advisory_count": len(findings),
            "affected": states.count("affected"),
            "fixed": states.count("fixed"),
            "unknown": states.count("unknown"),
            "mitigation_required": states.count("mitigation_required"),
            "mitigated": states.count("mitigated")
        },
        "findings": findings,
        "limitations": [
            "CLI version may differ from serving runtime.",
            "Version checks cannot reliably detect vendor backports.",
            "Local advisory data is not exhaustive.",
            "Static INI files do not prove the effective configuration of every serving worker."
        ]
    }


def format_json(report):
    return json.dumps(report, indent=2, sort_keys=True)


def format_text(report):
    project = report["project"]
    version = project.get("cli_runtime", {}).get("version") or "not detected"
    summary = report["summary"]
    lines = [
        "PHP PatchGuide",
        "Project: " + project.get("path", "?"),
        "PHP project detected: " + ("yes" if project.get("is_php_project") else "not confirmed"),
        "PHP CLI version: " + version,
    ]

    composer = project.get("composer", {})
    if composer.get("present"):
        lines.append("Composer package: " + (composer.get("name") or "not declared"))
        lines.append("Composer PHP requirement: " + (composer.get("require_php") or "not declared"))
        lines.append("Composer platform PHP: " + (composer.get("platform_php") or "not declared"))
    if composer.get("error"):
        lines.append("Composer metadata warning: " + composer["error"])

    for image in project.get("docker_php_images", []):
        lines.append("Docker PHP image: {} ({})".format(image.get("tag", "?"), image.get("file", "?")))
    for name, value in sorted(project.get("pinned_versions", {}).items()):
        lines.append("PHP version pin: {} = {}".format(name, value or "empty"))

    lines.extend([
        "PHP files discovered: " + str(project.get("php_file_count", 0)),
        "INI files discovered: " + str(len(project.get("php_ini_files", []))),
        "Advisory findings: " + str(summary["advisory_count"]),
        "Affected: {affected} | Fixed: {fixed} | Unknown: {unknown}".format(**summary),
        "Mitigation required: {mitigation_required} | Mitigation configured: {mitigated}".format(**summary),
        ""
    ])
    if not report["findings"]:
        lines.append("No local advisory records were loaded.")
    for item in report["findings"]:
        lines.append("{} {} [{}] {}".format(
            item["severity"].upper(), item["id"], item["status"], item["message"]))
        if item.get("url"):
            lines.append("         Source: " + item["url"])
    lines.extend([
        "",
        "Runtime note: " + project.get("runtime_warning", ""),
        "Configuration note: " + project.get("config_warning", ""),
        "Verify official vendor guidance before upgrading."
    ])
    return "\n".join(lines)
