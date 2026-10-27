"""Dependency-free PHP version parsing."""
import re

_PATTERN = re.compile(r"(?<!\d)(\d+)\.(\d+)\.(\d+)(?:[-+][0-9A-Za-z.-]+)?")
_PRERELEASE = re.compile(r"(?<![A-Za-z0-9])(dev|alpha|beta|rc)\.?\d*\b", re.I)


def parse_version(value):
    if not value:
        return None
    match = _PATTERN.search(value.strip())
    return tuple(map(int, match.groups())) if match else None


def compare_versions(left, right):
    """Compare numeric PHP versions, treating a recognized prerelease as older than stable."""
    a, b = parse_version(left or ""), parse_version(right or "")
    if a is None or b is None:
        return None
    if a != b:
        return (a > b) - (a < b)

    left_pre = bool(_PRERELEASE.search(str(left)))
    right_pre = bool(_PRERELEASE.search(str(right)))
    if left_pre != right_pre:
        return -1 if left_pre else 1
    return 0
