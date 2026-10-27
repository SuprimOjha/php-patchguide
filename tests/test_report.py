import unittest

from patchguide.report import build_report, format_json, format_text


class ReportTests(unittest.TestCase):
    def setUp(self):
        self.project = {
            "path": "/tmp/example",
            "is_php_project": True,
            "cli_runtime": {"version": "8.4.27"},
            "composer": {
                "present": True,
                "name": "demo/app",
                "require_php": "^8.2",
                "platform_php": "8.2.20",
                "error": None,
            },
            "docker_php_images": [{"file": "Dockerfile", "tag": "8.4.27-fpm-alpine"}],
            "pinned_versions": {".php-version": "8.4.27"},
            "php_file_count": 3,
            "php_ini_files": ["php.ini"],
            "runtime_warning": "CLI can differ from production.",
            "config_warning": "Static INI evidence only.",
        }

    def test_summary_counts_findings(self):
        report = build_report(self.project, [
            {"status": "affected"}, {"status": "fixed"}, {"status": "unknown"},
            {"status": "mitigation_required"}, {"status": "mitigated"},
        ])
        self.assertEqual(report["summary"]["affected"], 1)
        self.assertEqual(report["summary"]["fixed"], 1)
        self.assertEqual(report["summary"]["unknown"], 1)
        self.assertEqual(report["summary"]["mitigation_required"], 1)
        self.assertEqual(report["summary"]["mitigated"], 1)

    def test_json_output_is_valid(self):
        report = build_report(self.project, [])
        import json
        decoded = json.loads(format_json(report))
        self.assertEqual(decoded["project"]["composer"]["name"], "demo/app")

    def test_text_report_includes_project_metadata(self):
        report = build_report(self.project, [])
        text = format_text(report)
        self.assertIn("Composer PHP requirement: ^8.2", text)
        self.assertIn("Docker PHP image: 8.4.27-fpm-alpine", text)
        self.assertIn("PHP version pin: .php-version = 8.4.27", text)
        self.assertIn("PHP files discovered: 3", text)


if __name__ == "__main__":
    unittest.main()
