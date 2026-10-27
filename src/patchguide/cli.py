"""PatchGuide command-line interface."""
import argparse
import json
import sys
from pathlib import Path

from patchguide import __version__
from patchguide.advisories import find_advisory, load_advisories
from patchguide.checks import evaluate_advisories
from patchguide.project import inspect_project
from patchguide.report import build_report, format_json, format_text


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="patchguide",
        description="Read-only PHP security diagnostics",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    check = sub.add_parser("check", help="inspect a PHP project")
    check.add_argument("path", nargs="?", default=".")
    check.add_argument("--json", dest="json_path", metavar="FILE",
                       help="write JSON to FILE, or use '-' for stdout")
    check.add_argument("--advisories-dir", help="load reviewed advisory JSON from this directory")
    check.add_argument("--fail-on", choices=("never", "affected", "unknown", "mitigation-required"),
                       default="never",
                       help="exit 1 for affected findings, unknown status, or required mitigations")

    adv = sub.add_parser("advisories", help="inspect bundled advisory records")
    asp = adv.add_subparsers(dest="advisory_command", required=True)
    asp.add_parser("list", help="list all local records")
    show = asp.add_parser("show", help="show one local record")
    show.add_argument("identifier")
    sub.add_parser("version", help="print installed version")

    args = parser.parse_args(argv)
    try:
        if args.command == "version":
            print("PHP PatchGuide " + __version__)
            return 0

        if args.command == "advisories":
            records = load_advisories()
            if args.advisory_command == "list":
                for item in records:
                    print("{}  {:8}  {}".format(
                        item["id"], item.get("severity", "unknown").upper(),
                        item.get("title", "")))
                if not records:
                    print("No advisory records found.")
                return 0
            item = find_advisory(args.identifier)
            if item is None:
                print("Advisory not found: " + args.identifier, file=sys.stderr)
                return 2
            print(json.dumps(item, indent=2, sort_keys=True))
            return 0

        project = inspect_project(args.path)
        findings = evaluate_advisories(
            project["cli_runtime"].get("version"),
            load_advisories(args.advisories_dir),
            project["php_ini_settings"],
        )
        report = build_report(project, findings)
        if args.json_path == "-":
            print(format_json(report))
        else:
            print(format_text(report))
            if args.json_path:
                target = Path(args.json_path).expanduser()
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(format_json(report) + "\n", encoding="utf-8")
                print("JSON report written to " + str(target.resolve()))

        if args.fail_on == "affected" and report["summary"]["affected"]:
            return 1
        if args.fail_on == "unknown" and report["summary"]["unknown"]:
            return 1
        if args.fail_on == "mitigation-required" and report["summary"]["mitigation_required"]:
            return 1
        return 0
    except (OSError, ValueError) as exc:
        print("patchguide: error: " + str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
