import unittest
from patchguide.versions import compare_versions, parse_version
class VersionTests(unittest.TestCase):
    def test_parse(self): self.assertEqual(parse_version("PHP 8.5.12 (cli)"),(8,5,12))
    def test_invalid(self): self.assertIsNone(parse_version("unknown"))
    def test_compare(self):
        self.assertEqual(compare_versions("8.4.26","8.4.27"),-1)
        self.assertEqual(compare_versions("8.4.27","8.4.27"),0)
        self.assertEqual(compare_versions("8.5.1","8.4.99"),1)
if __name__=="__main__": unittest.main()
