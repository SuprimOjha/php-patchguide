"""Load and minimally validate local advisory JSON files."""
import json
import re
from pathlib import Path

_ID_PATTERN = re.compile(r"^CVE-\d{4}-\d{4,}$")
_VERSION_PATTERN = re.compile(r"^\d+\.\d+\.\d+$")
_BRANCH_PATTERN = re.compile(r"^\d+\.\d+$")


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
        kind = item.get("kind", "version")
        if kind not in {"version", "mitigation"}:
            raise ValueError(f"Advisory {path} has unsupported kind: {kind!r}")
        mitigation_only = kind == "mitigation"
        fixed_by = item.get("fixed_by", {})
        if not isinstance(identifier, str) or not _ID_PATTERN.fullmatch(identifier):
            raise ValueError(f"Advisory {path} has an invalid CVE id")
        if identifier in seen:
            raise ValueError(f"Duplicate advisory id {identifier} in {root}")
        if not mitigation_only and (not isinstance(fixed_by, dict) or not fixed_by):
            raise ValueError(f"Advisory {path} must include a non-empty fixed_by object")
        if mitigation_only and fixed_by != {}:
            raise ValueError(f"Mitigation-only advisory {path} must not claim fixed versions")
        for branch, version in fixed_by.items():
            if not isinstance(branch, str) or not _BRANCH_PATTERN.fullmatch(branch):
                raise ValueError(f"Advisory {path} has invalid PHP branch key: {branch!r}")
            if not isinstance(version, str) or not _VERSION_PATTERN.fullmatch(version):
                raise ValueError(f"Advisory {path} has invalid fixed version for {branch}")
        url = item.get("url")
        if not isinstance(url, str) or not url.startswith(("https://", "http://")):
            raise ValueError(f"Advisory {path} must include an HTTP(S) url")
        if not isinstance(item.get("title"), str) or not item["title"].strip():
            raise ValueError(f"Advisory {path} must include a title")
        seen.add(identifier)
        items.append(item)
    return items


def find_advisory(identifier, directory=None):
    target = identifier.strip().upper()
    return next((item for item in load_advisories(directory)
                 if item.get("id", "").upper() == target), None)
