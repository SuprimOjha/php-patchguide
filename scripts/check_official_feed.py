"""Snapshot the official PHP archive and flag CVEs not in the local advisory database."""
import argparse
import html
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

YEAR = datetime.now(timezone.utc).year
URL = f"https://www.php.net/archive/{YEAR}.php"


def summarize(page, local_ids=None):
    text = html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", page)))
    cves = sorted(set(re.findall(r"CVE-\d{4}-\d{4,}", text)))
    local = sorted(set(local_ids or []))
    return {
        "source": URL,
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "latest_release_mention": (lambda match: match.group(0) if match else None)(
            re.search(r"PHP\s+(\d+\.\d+\.\d+)\s+Released", text, re.I)),
        "cve_identifiers_seen": cves,
        "cve_identifiers_not_in_local_database": sorted(set(cves) - set(local)),
        "local_cve_identifiers_not_seen_in_archive": sorted(set(local) - set(cves)),
        "note": "Snapshot and discrepancy report only. Review official records manually; this script does not create or update advisory records."
    }


def read_local_ids(directory):
    root = Path(directory)
    ids = []
    for path in sorted(root.glob("CVE-*.json")):
        try:
            item = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise ValueError(f"Cannot read advisory {path}: {exc}") from exc
        if isinstance(item, dict) and isinstance(item.get("id"), str):
            ids.append(item["id"])
    return ids


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", default="-", help="output JSON path, or '-' for stdout")
    parser.add_argument("--advisories-dir", default="advisories",
                        help="local advisory directory used for discrepancy reporting")
    args = parser.parse_args(argv)
    try:
        request = Request(URL, headers={"User-Agent": "PHP-PatchGuide-FeedMonitor/0.2"})
        with urlopen(request, timeout=15) as response:
            data = response.read(2_000_000).decode("utf-8", errors="replace")
        report = summarize(data, read_local_ids(args.advisories_dir))
        output = json.dumps(report, indent=2, sort_keys=True) + "\n"
        if args.output == "-":
            print(output, end="")
        else:
            target = Path(args.output)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(output, encoding="utf-8")
            print("Snapshot written to " + str(target))
        if report["cve_identifiers_not_in_local_database"]:
            print("Review required: archive contains CVE IDs absent from the local database.",
                  file=sys.stderr)
        return 0
    except (OSError, ValueError) as exc:
        print("feed monitor failed: " + str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
