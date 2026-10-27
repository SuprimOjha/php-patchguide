import tempfile
import unittest
from pathlib import Path

from patchguide.project import inspect_project


class ProjectInspectionTests(unittest.TestCase):
    def test_fixture_detects_composer_and_docker(self):
        fixture = Path(__file__).parent / "fixtures"
        result = inspect_project(fixture)
        self.assertTrue(result["is_php_project"])
        self.assertTrue(result["composer"]["present"])
        self.assertEqual(result["composer"]["require_php"], "^8.2")
        self.assertEqual(result["composer"]["platform_php"], "8.2.20")
        self.assertTrue(any(item["tag"] == "8.4.26-fpm-alpine"
                            for item in result["docker_php_images"]))

    def test_ini_setting_is_detected(self):
        with tempfile.TemporaryDirectory() as directory:
            Path(directory, "php.ini").write_text(
                "; comment\nsession.upload_progress.enabled = Off\n", encoding="utf-8")
            result = inspect_project(directory)
            self.assertEqual(result["php_ini_settings"]["session.upload_progress.enabled"][0]["value"], "off")

    def test_missing_directory_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(ValueError):
                inspect_project(Path(directory) / "does-not-exist")


if __name__ == "__main__":
    unittest.main()
