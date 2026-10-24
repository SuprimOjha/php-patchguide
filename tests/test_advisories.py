import json, tempfile, unittest
from pathlib import Path
from patchguide.advisories import load_advisories, find_advisory
from patchguide.checks import evaluate_advisories
SAMPLE={"id":"CVE-2099-12345","title":"Test","severity":"high","fixed_by":{"8.4":"8.4.27"},"url":"https://example.invalid"}
class AdvisoryTests(unittest.TestCase):
    def test_load_and_find(self):
        with tempfile.TemporaryDirectory() as d:
            Path(d,"CVE-2099-12345.json").write_text(json.dumps(SAMPLE),encoding="utf-8")
            self.assertEqual(len(load_advisories(d)),1)
            self.assertEqual(find_advisory("cve-2099-12345",d)["id"],SAMPLE["id"])
    def test_statuses(self):
        self.assertEqual(evaluate_advisories("8.4.26",[SAMPLE])[0]["status"],"affected")
        self.assertEqual(evaluate_advisories("8.4.27",[SAMPLE])[0]["status"],"fixed")
        self.assertEqual(evaluate_advisories(None,[SAMPLE])[0]["status"],"unknown")
        self.assertEqual(evaluate_advisories("8.1.2",[SAMPLE])[0]["status"],"unknown")
if __name__=="__main__": unittest.main()
