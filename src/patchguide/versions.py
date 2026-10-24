"""Dependency-free PHP version parsing."""
import re
_PATTERN = re.compile(r"(?<!\d)(\d+)\.(\d+)\.(\d+)(?:[-+][0-9A-Za-z.-]+)?")

def parse_version(value):
    if not value:
        return None
    match = _PATTERN.search(value.strip())
    return tuple(map(int, match.groups())) if match else None

def compare_versions(left, right):
    a, b = parse_version(left or ""), parse_version(right or "")
    if a is None or b is None:
        return None
    return (a > b) - (a < b)
