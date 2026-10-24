"""PatchGuide command-line interface."""
import argparse, json, sys
from pathlib import Path
from patchguide import __version__
from patchguide.advisories import find_advisory, load_advisories
from patchguide.checks import evaluate_advisories
from patchguide.project import inspect_project
from patchguide.report import build_report, format_json, format_text

def main(argv=None):
    parser=argparse.ArgumentParser(prog="patchguide",description="Read-only PHP security diagnostics")
    sub=parser.add_subparsers(dest="command",required=True)
    check=sub.add_parser("check"); check.add_argument("path",nargs="?",default="."); check.add_argument("--json",dest="json_path"); check.add_argument("--advisories-dir")
    adv=sub.add_parser("advisories"); asp=adv.add_subparsers(dest="advisory_command",required=True); asp.add_parser("list"); show=asp.add_parser("show"); show.add_argument("identifier"); sub.add_parser("version")
    args=parser.parse_args(argv)
    try:
        if args.command=="version":
            print("PHP PatchGuide "+__version__); return 0
        if args.command=="advisories":
            records=load_advisories()
            if args.advisory_command=="list":
                for x in records: print("{}  {:8}  {}".format(x["id"],x.get("severity","unknown").upper(),x.get("title","")))
                if not records: print("No advisory records found.")
                return 0
            item=find_advisory(args.identifier)
            if item is None: print("Advisory not found: "+args.identifier,file=sys.stderr); return 2
            print(json.dumps(item,indent=2,sort_keys=True)); return 0
        project=inspect_project(args.path)
        findings=evaluate_advisories(project["cli_runtime"].get("version"),load_advisories(args.advisories_dir))
        report=build_report(project,findings)
        if args.json_path=="-": print(format_json(report))
        else:
            print(format_text(report))
            if args.json_path:
                target=Path(args.json_path).expanduser(); target.parent.mkdir(parents=True,exist_ok=True); target.write_text(format_json(report)+"\n",encoding="utf-8"); print("JSON report written to "+str(target.resolve()))
        return 0
    except (OSError,ValueError) as exc:
        print("patchguide: error: "+str(exc),file=sys.stderr); return 2
if __name__=="__main__": raise SystemExit(main())
