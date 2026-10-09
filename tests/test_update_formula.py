"""Contract tests for the release-to-formula updater."""
import importlib.util
from pathlib import Path
import unittest
import re

ROOT = Path(__file__).resolve().parents[1]


class UpdateFormulaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location("updater", ROOT / "scripts/update_formula.py")
        cls.updater = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.updater)

    def fixture(self, tool="khsier", tag="v1.2.3"):
        names = self.updater.asset_names(tool, tag)
        release = {"tag_name": tag, "draft": False, "prerelease": False,
                   "assets": [{"name": name, "browser_download_url": f"https://github.com/zaubermaerchen/{tool}/releases/download/{tag}/{name}"} for name in names + ["SHA256SUMS"]]}
        checksums = "\n".join(f"{str(i + 1) * 64}  {name}" for i, name in enumerate(names))
        return release, checksums

    def test_update_preserves_all_other_formula_content_and_is_idempotent(self):
        for tool in ("khsier", "pipewisp", "dam", "outage", "sluice", "trysudo"):
            with self.subTest(tool=tool):
                original = (ROOT / "Formula" / f"{tool}.rb").read_text()
                release, sums = self.fixture(tool)
                updated = self.updater.update_formula(original, tool, "v1.2.3", release, sums)
                def metadata(text):
                    return re.sub(r'^(  version|      url|      sha256) "[^"\n]+"$', r'\1 "<release>"', text, flags=re.M)
                self.assertEqual(metadata(updated), metadata(original))
                self.assertIn('version "1.2.3"', updated)
                self.assertEqual(updated, self.updater.update_formula(updated, tool, "v1.2.3", release, sums))
                for i, name in enumerate(self.updater.asset_names(tool, "v1.2.3")):
                    self.assertIn(f'url "https://github.com/zaubermaerchen/{tool}/releases/download/v1.2.3/{name}"\n      sha256 "{str(i + 1) * 64}"', updated)

    def test_rejects_unpublished_or_incomplete_release(self):
        for field in ("draft", "prerelease"):
            release, sums = self.fixture()
            release[field] = True
            with self.assertRaises(ValueError):
                self.updater.update_formula((ROOT / "Formula/khsier.rb").read_text(), "khsier", "v1.2.3", release, sums)
        release, sums = self.fixture()
        release["assets"].pop(0)
        with self.assertRaises(ValueError):
            self.updater.validate_release("khsier", "v1.2.3", release)

    def test_rejects_bad_checksum_manifest(self):
        release, sums = self.fixture()
        for invalid in (sums + "\n" + sums.splitlines()[0], sums.replace("1" * 64, "xyz"), "\n".join(sums.splitlines()[1:]), sums.replace("khsier_v", "../khsier_v")):
            with self.subTest(invalid=invalid), self.assertRaises(ValueError):
                self.updater.update_formula((ROOT / "Formula/khsier.rb").read_text(), "khsier", "v1.2.3", release, invalid)

    def test_rejects_injection_and_unexpected_formula_shape(self):
        for tool, tag in (("../khsier", "v1.2.3"), ("khsier", 'v1.2.3";system("evil")'), ("khsier", "v1.2.3-rc1")):
            with self.assertRaises(ValueError):
                self.updater.asset_names(tool, tag)
        release, sums = self.fixture()
        original = (ROOT / "Formula/khsier.rb").read_text()
        with self.assertRaises(ValueError):
            self.updater.update_formula(original.replace("darwin_arm64", "windows_arm64"), "khsier", "v1.2.3", release, sums)

    def test_rejects_release_older_than_formula(self):
        release, sums = self.fixture(tag="v0.1.0")
        with self.assertRaisesRegex(ValueError, "older"):
            self.updater.update_formula((ROOT / "Formula/khsier.rb").read_text(), "khsier", "v0.1.0", release, sums)

    def test_rejects_asset_url_outside_expected_release(self):
        release, _ = self.fixture()
        release["assets"][0]["browser_download_url"] = "https://example.com/payload"
        with self.assertRaises(ValueError):
            self.updater.validate_release("khsier", "v1.2.3", release)


if __name__ == "__main__":
    unittest.main()
