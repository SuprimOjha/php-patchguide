"""Load and minimally validate local advisory JSON files."""
import json
import re
from pathlib import Path


_ID_PATTERN = re.compile(r"^CVE-\d{4}-\d{4,}$")


def default_advisory_dir():
    checkout = Path(__file__).resolve().parents[2] / "advisories"
    if checkout.is_dir():
        return checkout
    return Path(__file__).resolve().parent / "data" / "advisories"


def load_advisories(directory=None):
    root = Path(directory).expanduser() if directory else default_advisory_dir()
    if not root.is_dir():
        raise ValueError(f"Advisory directory does not exist or is not a directory: {root}")

    items = []
    seen = set()
    for path in sorted(root.glob("CVE-*.json")):
        try:
            item = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise ValueError(f"Cannot load {path}: {exc}") from exc
        if not isinstance(item, dict):
            raise ValueError(f"Advisory {path} must contain a JSON object")
        identifier = item.get("id")
        fixed_by = item.get("fixed_by")
        if not isinstance(identifier, str) or not _ID_PATTERN.fullmatch(identifier):
            raise ValueError(f"Advisory {path} has an invalid CVE id")
        if identifier in seen:
            raise ValueError(f"Duplicate advisory id {identifier} in {root}")
        if not isinstance(fixed_by, dict) or not fixed_by:
            raise ValueError(f"Advisory {path} must include a non-empty fixed_by object")
        for branch, version in fixed_by.items():
            if not isinstance(branch, str) or not re.fullmatch(r"\d+\.\d+", branch):
                raise ValueError(f"Advisory {path} has invalid PHP branch key: {branch!r}")
            if not isinstance(version, str) or not re.fullmatch(r"\d+\.\d+\.\d+", version):
                raise ValueError(f"Advisory {path} has invalid fixed version for {branch}")
        if not isinstance(item.get("url"), str) or not item["url"].startswith(("https://", "http://")):
            raise ValueError(f"Advisory {path} must include an HTTP(S) url")
        seen.add(identifier)
        items.append(item)
    return items


def find_advisory(identifier, directory=None):
    target = identifier.strip().upper()
    return next((item for item in load_advisories(directory)
                 if item.get("id", "").upper() == target), None)
