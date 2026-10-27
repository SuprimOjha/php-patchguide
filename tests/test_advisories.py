import json
import tempfile
import unittest
from pathlib import Path

from patchguide.advisories import load_advisories, find_advisory
from patchguide.checks import evaluate_advisories

SAMPLE = {
    "id": "CVE-2099-12345",
    "title": "Test",
    "severity": "high",
    "fixed_by": {"8.4": "8.4.27"},
    "url": "https://example.invalid/advisory",
}


class AdvisoryTests(unittest.TestCase):
    def test_load_and_find(self):
        with tempfile.TemporaryDirectory() as directory:
            Path(directory, "CVE-2099-12345.json").write_text(
                json.dumps(SAMPLE), encoding="utf-8")
            self.assertEqual(len(load_advisories(directory)), 1)
            self.assertEqual(find_advisory("cve-2099-12345", directory)["id"], SAMPLE["id"])

    def test_invalid_directory_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(ValueError, "does not exist"):
                load_advisories(Path(directory) / "missing")

    def test_invalid_advisory_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            Path(directory, "CVE-2099-12345.json").write_text(
                json.dumps({"id": "not-a-cve", "fixed_by": {"8.4": "8.4.27"},
                            "url": "https://example.invalid"}),
                encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "invalid CVE id"):
                load_advisories(directory)

    def test_packaged_and_checkout_advisories_match(self):
        root = Path(__file__).resolve().parents[1]
        def read_records(directory):
            return {p.name: json.loads(p.read_text(encoding="utf-8"))
                    for p in directory.glob("CVE-*.json")}
        self.assertEqual(read_records(root / "advisories"),
                         read_records(root / "src" / "patchguide" / "data" / "advisories"))

    def test_version_statuses(self):
        self.assertEqual(evaluate_advisories("8.4.26", [SAMPLE])[0]["status"], "affected")
        self.assertEqual(evaluate_advisories("8.4.27", [SAMPLE])[0]["status"], "fixed")
        self.assertEqual(evaluate_advisories(None, [SAMPLE])[0]["status"], "unknown")
        self.assertEqual(evaluate_advisories("8.1.2", [SAMPLE])[0]["status"], "unknown")

    def test_mitigation_only_record_never_claims_fixed_version(self):
        record = {"id": "CVE-2099-12346", "kind": "mitigation", "title": "Mitigation",
                  "severity": "high", "fixed_by": {},
                  "url": "https://example.invalid/advisory"}
        settings = {"session.upload_progress.enabled": [{"file": "php.ini", "value": "1"}]}
        finding = evaluate_advisories("8.4.27", [record], settings)[0]
        self.assertEqual(finding["status"], "mitigation_required")
        self.assertIsNone(finding["fixed_version"])

    def test_disabled_setting_is_reported_as_mitigated(self):
        record = {"id": "CVE-2099-12346", "kind": "mitigation", "title": "Mitigation",
                  "severity": "high", "fixed_by": {},
                  "url": "https://example.invalid/advisory"}
        settings = {"session.upload_progress.enabled": [{"file": "php.ini", "value": "0"}]}
        self.assertEqual(evaluate_advisories("8.4.27", [record], settings)[0]["status"], "mitigated")


if __name__ == "__main__":
    unittest.main()
