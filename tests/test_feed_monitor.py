import importlib.util
import unittest
from pathlib import Path
script = Path(__file__).resolve().parents[1] / "scripts" / "check_official_feed.py"
spec = importlib.util.spec_from_file_location("feed_monitor", script)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
class FeedMonitorTests(unittest.TestCase):
    def test_extracts_release_and_cves(self):
        report = module.summarize("<h2>PHP 8.5.12 Released!</h2><p>CVE-2026-109618 CVE-2026-109619</p>")
        self.assertIn("8.5.12", report["latest_release_mention"])
        self.assertEqual(report["cve_identifiers_seen"], ["CVE-2026-109618", "CVE-2026-109619"])
if __name__ == "__main__":
    unittest.main()
