"""Exercise target selection against real PR-style Git histories."""
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/select_formulae.py'
spec = importlib.util.spec_from_file_location('selector', SCRIPT)
selector = importlib.util.module_from_spec(spec)
spec.loader.exec_module(selector)


class SelectFormulaeTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        (self.root / 'Formula').mkdir()
        for formula in ('dam', 'trysudo'):
            (self.root / f'Formula/{formula}.rb').write_text('original\n')
        self.git('init', '-q')
        self.base = self.commit()

    def git(self, *args):
        return subprocess.run(['git', *args], cwd=self.root, check=True,
                              capture_output=True, text=True).stdout.strip()

    def commit(self):
        self.git('add', '-A')
        self.git('-c', 'user.name=Test', '-c', 'user.email=test@example.invalid',
                 '-c', 'commit.gpgsign=false', 'commit', '-qm', 'Fixture')
        return self.git('rev-parse', 'HEAD')

    def select(self, base=None):
        return selector.select_formulae(self.root, 'pull_request',
                                       base=base or self.base, head=self.git('rev-parse', 'HEAD'))

    def test_single_multiple_and_new_formulae(self):
        (self.root / 'Formula/trysudo.rb').write_text('updated\n')
        self.commit()
        self.assertEqual(self.select(), ['trysudo'])
        (self.root / 'Formula/dam.rb').write_text('updated\n')
        (self.root / 'Formula/new-tool.rb').write_text('new\n')
        self.commit()
        self.assertEqual(self.select(), ['dam', 'new-tool', 'trysudo'])

    def test_no_change_documentation_and_deletion_skip_brew(self):
        self.assertEqual(self.select(), [])
        (self.root / 'README.md').write_text('docs\n')
        (self.root / 'docs').mkdir()
        (self.root / 'docs/guide.md').write_text('docs\n')
        self.commit()
        self.assertEqual(self.select(), [])
        (self.root / 'Formula/dam.rb').unlink()
        self.commit()
        self.assertEqual(self.select(), [])

    def test_renamed_formula_selects_only_new_name(self):
        (self.root / 'Formula/dam.rb').rename(self.root / 'Formula/new-tool.rb')
        self.commit()
        self.assertEqual(self.select(), ['new-tool'])

    def test_shared_changes_select_all(self):
        for name in ('.github/workflows/test.yml', '.github/actions/setup/action.yml',
                     'scripts/check.py', 'tests/test_check.py', 'config.json'):
            with self.subTest(name=name):
                path = self.root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text('shared\n')
                self.commit()
                self.assertEqual(self.select(), ['dam', 'trysudo'])
                self.git('reset', '--hard', self.base)

    def test_merge_base_excludes_changes_only_on_base_branch(self):
        (self.root / 'Formula/trysudo.rb').write_text('PR\n')
        head = self.commit()
        self.git('checkout', '--detach', self.base)
        (self.root / 'Formula/dam.rb').write_text('base advanced\n')
        base = self.commit()
        self.git('checkout', '--detach', head)
        self.assertEqual(self.select(base), ['trysudo'])

    def test_failed_diff_falls_back_to_all(self):
        for base in ('', 'invalid', '0' * 40):
            with self.subTest(base=base):
                self.assertEqual(selector.select_formulae(
                    self.root, 'pull_request', base=base, head=self.base), ['dam', 'trysudo'])
        for output in (b'Formula/dam.rb', b'\xff\0'):
            with self.subTest(output=output), patch.object(selector.subprocess, 'run') as run:
                run.return_value.stdout = output
                self.assertEqual(selector.select_formulae(
                    self.root, 'pull_request', base=self.base, head=self.base), ['dam', 'trysudo'])

    def test_push_and_manual_selection_use_current_files(self):
        (self.root / 'Formula/new-tool.rb').write_text('new\n')
        for event in ('push', 'workflow_dispatch'):
            self.assertEqual(selector.select_formulae(self.root, event), ['dam', 'new-tool', 'trysudo'])
        self.assertEqual(selector.select_formulae(self.root, 'workflow_dispatch', 'trysudo'), ['trysudo'])
        for name in ('unknown', '../dam', 'dam,trysudo', 'dam\n', '$(echo dam)'):
            with self.subTest(name=name), self.assertRaisesRegex(ValueError, 'Unknown formula'):
                selector.select_formulae(self.root, 'workflow_dispatch', name)

    def test_cli_emits_json_and_rejects_invalid_manual_input(self):
        for formula, success in (('', True), ('trysudo', True), ('invalid', False)):
            result = subprocess.run(['python3', str(SCRIPT)], cwd=self.root,
                                    env=dict(os.environ, GITHUB_EVENT_NAME='workflow_dispatch', FORMULA=formula),
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode == 0, success, result.stderr)
            if success:
                self.assertEqual(json.loads(result.stdout), [formula] if formula else ['dam', 'trysudo'])
            else:
                self.assertIn('Unknown formula', result.stderr)
                self.assertEqual(result.stdout, '')


if __name__ == '__main__':
    unittest.main()
