import io, tempfile, unittest
from contextlib import redirect_stdout
from patchguide.cli import main
class CliTests(unittest.TestCase):
    def test_version(self):
        out=io.StringIO()
        with redirect_stdout(out): code=main(["version"])
        self.assertEqual(code,0); self.assertIn("PHP PatchGuide",out.getvalue())
    def test_list(self):
        out=io.StringIO()
        with redirect_stdout(out): code=main(["advisories","list"])
        self.assertEqual(code,0); self.assertIn("CVE-2026-109618",out.getvalue())
    def test_json(self):
        with tempfile.TemporaryDirectory() as d:
            out=io.StringIO()
            with redirect_stdout(out): code=main(["check",d,"--json","-"])
            self.assertEqual(code,0); self.assertIn('"findings"',out.getvalue())
if __name__=="__main__": unittest.main()
