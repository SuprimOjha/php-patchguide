import importlib.util
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "check_official_feed.py"
SPEC = importlib.util.spec_from_file_location("patchguide_feed_monitor", SCRIPT)
MONITOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MONITOR)


class FeedMonitorTests(unittest.TestCase):
    def test_reports_cves_missing_from_local_database(self):
        report = MONITOR.summarize(
            "<h2>CVE-2026-111111</h2><p>CVE-2026-222222</p>",
            ["CVE-2026-111111"])
        self.assertEqual(report["cve_identifiers_not_in_local_database"],
                         ["CVE-2026-222222"])
        self.assertEqual(report["local_cve_identifiers_not_seen_in_archive"], [])

    def test_reports_local_ids_not_seen_in_archive(self):
        report = MONITOR.summarize(
            "<p>CVE-2026-111111</p>",
            ["CVE-2026-111111", "CVE-2026-222222"])
        self.assertEqual(report["local_cve_identifiers_not_seen_in_archive"],
                         ["CVE-2026-222222"])

    def test_html_entities_are_decoded(self):
        report = MONITOR.summarize(
            "<p>PHP 8.5.12 Released &amp; CVE-2026-111111</p>", [])
        self.assertEqual(report["latest_release_mention"], "PHP 8.5.12 Released")
        self.assertEqual(report["cve_identifiers_seen"], ["CVE-2026-111111"])


if __name__ == "__main__":
    unittest.main()
