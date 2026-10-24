"""Load local advisory JSON files."""
import json
from pathlib import Path

def default_advisory_dir():
    return Path(__file__).resolve().parents[2] / "advisories"

def load_advisories(directory=None):
    root = Path(directory) if directory else default_advisory_dir()
    if not root.is_dir():
        return []
    items = []
    for path in sorted(root.glob("CVE-*.json")):
        try:
            item = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise ValueError(f"Cannot load {path}: {exc}") from exc
        if not isinstance(item, dict) or not item.get("id") or not item.get("fixed_by"):
            raise ValueError(f"Advisory {path} lacks id/fixed_by")
        items.append(item)
    return items

def find_advisory(identifier, directory=None):
    target = identifier.strip().upper()
    return next((x for x in load_advisories(directory) if x.get("id", "").upper() == target), None)
