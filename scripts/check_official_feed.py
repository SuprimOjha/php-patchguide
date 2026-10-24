"""Snapshot the public PHP archive for manual review."""
import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

URL = "https://www.php.net/archive/2026.php"

def summarize(html):
    text = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", html))
    release = re.search(r"PHP\s+(\d+\.\d+\.\d+)\s+Released", text, re.I)
    cves = sorted(set(re.findall(r"CVE-\d{4}-\d{4,}", text)))
    return {"source": URL, "checked_at": datetime.now(timezone.utc).isoformat(),
            "latest_release_mention": release.group(0) if release else None,
            "cve_identifiers_seen": cves,
            "note": "Snapshot only; review official advisories manually."}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", default="-")
    args = parser.parse_args()
    try:
        request = Request(URL, headers={"User-Agent": "PHP-PatchGuide-FeedMonitor/0.1"})
        with urlopen(request, timeout=15) as response:
            data = response.read(2000000).decode("utf-8", errors="replace")
        output = json.dumps(summarize(data), indent=2) + "\n"
        if args.output == "-":
            print(output, end="")
        else:
            target = Path(args.output)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(output, encoding="utf-8")
            print("Snapshot written to " + str(target))
        return 0
    except Exception as exc:
        print("feed monitor failed: " + str(exc), file=sys.stderr)
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
