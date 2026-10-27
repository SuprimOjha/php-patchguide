import io
import json
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest.mock import patch

from patchguide.cli import main


class CliTests(unittest.TestCase):
    def test_version(self):
        out = io.StringIO()
        with redirect_stdout(out):
            code = main(["version"])
        self.assertEqual(code, 0)
        self.assertIn("PHP PatchGuide", out.getvalue())

    def test_list(self):
        out = io.StringIO()
        with redirect_stdout(out):
            code = main(["advisories", "list"])
        self.assertEqual(code, 0)
        self.assertIn("CVE-2026-109618", out.getvalue())
        self.assertIn("CVE-2026-115560", out.getvalue())

    def test_json_stdout_is_parseable(self):
        with tempfile.TemporaryDirectory() as directory:
            out = io.StringIO()
            with redirect_stdout(out):
                code = main(["check", directory, "--json", "-"])
            self.assertEqual(code, 0)
            report = json.loads(out.getvalue())
            self.assertIn("findings", report)
            self.assertIn("summary", report)

    def test_json_file_is_created(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "nested" / "report.json"
            with redirect_stdout(io.StringIO()):
                code = main(["check", directory, "--json", str(target)])
            self.assertEqual(code, 0)
            self.assertTrue(target.is_file())
            self.assertIn("findings", json.loads(target.read_text(encoding="utf-8")))

    def test_missing_advisory_returns_two(self):
        err = io.StringIO()
        with redirect_stderr(err):
            code = main(["advisories", "show", "CVE-2099-00000"])
        self.assertEqual(code, 2)
        self.assertIn("Advisory not found", err.getvalue())

    def test_invalid_path_returns_two(self):
        err = io.StringIO()
        with redirect_stderr(err):
            code = main(["check", "path-that-should-not-exist-patchguide"])
        self.assertEqual(code, 2)

    def _run_with_finding(self, status, policy):
        project = {"path": "/tmp/demo", "cli_runtime": {"version": "8.4.26"},
                   "php_ini_settings": {}, "runtime_warning": "Test runtime",
                   "config_warning": "Test config"}
        finding = {"id": "CVE-2099-12345", "title": "Test", "severity": "high",
                   "status": status, "current_version": "8.4.26",
                   "fixed_version": None, "message": "Test finding",
                   "url": "https://example.invalid"}
        with patch("patchguide.cli.inspect_project", return_value=project), \
             patch("patchguide.cli.load_advisories", return_value=[]), \
             patch("patchguide.cli.evaluate_advisories", return_value=[finding]), \
             redirect_stdout(io.StringIO()):
            return main(["check", ".", "--fail-on", policy])

    def test_fail_on_affected_returns_one(self):
        self.assertEqual(self._run_with_finding("affected", "affected"), 1)

    def test_fail_on_unknown_returns_one(self):
        self.assertEqual(self._run_with_finding("unknown", "unknown"), 1)

    def test_fail_on_mitigation_required_returns_one(self):
        self.assertEqual(self._run_with_finding("mitigation_required", "mitigation-required"), 1)


if __name__ == "__main__":
    unittest.main()
