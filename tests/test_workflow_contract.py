"""Guard security ordering and generated-formula validation in the workflow."""
from pathlib import Path
import unittest
import os
import re
import subprocess
import tempfile
import textwrap

WORKFLOW = Path(__file__).resolve().parents[1] / '.github/workflows/update-formula.yml'


class WorkflowContractTests(unittest.TestCase):
    def test_normal_checks_cover_all_formulae_on_both_platforms(self):
        root = WORKFLOW.parents[2]
        workflow = (root / '.github/workflows/test.yml').read_text()
        brew = workflow.split('  brew:\n', 1)[1]
        selected = re.search(r'formula: \[([^\]]+)\]', brew)
        self.assertIsNotNone(selected, 'Native checks must select every formula')
        formulae = [name.strip() for name in selected.group(1).split(',')]
        self.assertCountEqual(formulae, [path.stem for path in (root / 'Formula').glob('*.rb')])
        self.assertIn('os: [ubuntu-latest, macos-latest]', brew)
        self.assertIn('runs-on: ${{ matrix.os }}', brew)
        self.assertIn('FORMULA: ${{ matrix.formula }}', brew)
        guard = 'test "$(git -C "$(brew --repository zaubermaerchen/tap)" rev-parse HEAD)" = "$GITHUB_SHA"'
        self.assertIn(guard, brew)
        self.assertLess(brew.index(guard), brew.index('brew install'))
        self.assertIn('brew install "zaubermaerchen/tap/$FORMULA"', brew)
        self.assertIn('brew test "zaubermaerchen/tap/$FORMULA"', brew)

    def test_caller_guard_allows_trysudo_and_rejects_other_sources(self):
        step = WORKFLOW.read_text().split('      - name: Validate caller and trusted revision\n', 1)[1]
        script = textwrap.dedent(step.split('        run: |\n', 1)[1].split('      - uses:', 1)[0])
        for formula, repository, ref, allowed in (
            ('trysudo', 'zaubermaerchen/trysudo', 'main', True),
            ('trysudo', 'zaubermaerchen/trysudo', 'a' * 40, True),
            ('trysudo', 'other/trysudo', 'main', False),
            ('trysudo', 'zaubermaerchen/sluice', 'main', False),
            ('unknown', 'zaubermaerchen/unknown', 'main', False),
            ('trysudo', 'zaubermaerchen/trysudo', 'unreviewed-branch', False),
        ):
            with self.subTest(formula=formula, repository=repository, ref=ref):
                environment = dict(os.environ, FORMULA=formula, SOURCE_REPOSITORY=repository,
                                   AUTOMATION_REF=ref)
                result = subprocess.run(['bash', '-e', '-o', 'pipefail', '-c', script],
                                        env=environment, capture_output=True, text=True)
                self.assertEqual(result.returncode == 0, allowed, result.stderr)

    def test_writer_waits_for_validation_and_uses_scoped_app(self):
        workflow = WORKFLOW.read_text()
        writer = workflow.split('  pull-request:\n', 1)[1]
        self.assertIn('needs: [prepare, brew-test]', writer)
        self.assertLess(writer.index('Reject changes to the verified formula base'), writer.index('actions/create-github-app-token'))
        self.assertIn('repositories: homebrew-tap', writer)
        self.assertIn('permission-contents: write', writer)
        self.assertIn('permission-pull-requests: write', writer)
        self.assertNotIn('contents: write', workflow.split('jobs:')[0])
        self.assertNotIn('scripts/update_formula.py', writer)
        self.assertIn('cmp "$RUNNER_TEMP/current-formula.rb" release-formula/base.rb', writer)
        self.assertIn('base: main', writer)
        self.assertIn('branch: automation/update-${{ inputs.formula }}-${{ inputs.tag }}', writer)

    def test_writer_base_guard_executes_and_rejects_drift(self):
        step = WORKFLOW.read_text().split('      - name: Reject changes to the verified formula base\n', 1)[1]
        script = textwrap.dedent(step.split('        run: |\n', 1)[1].split('      # Mint only', 1)[0])
        base = 'class Khsier < Formula\n  version "1.0.0"\n  desc "Original"\nend\n'
        candidate = base.replace('1.0.0', '1.2.3')
        for current in (base, base.replace('Original', 'Edited'), base.replace('1.0.0', '1.1.0')):
            with self.subTest(current=current), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                (root / 'Formula').mkdir()
                (root / 'release-formula').mkdir()
                formula = root / 'Formula/khsier.rb'
                formula.write_text(current)
                (root / 'release-formula/base.rb').write_text(base)
                (root / 'release-formula/candidate.rb').write_text(candidate)
                def git(*args):
                    subprocess.run(['git', *args], cwd=root, check=True, capture_output=True)
                git('init', '-q')
                git('add', 'Formula/khsier.rb')
                git('-c', 'user.name=Test', '-c', 'user.email=test@example.invalid',
                    '-c', 'commit.gpgsign=false', 'commit', '-qm', 'Fixture')
                environment = dict(os.environ, FORMULA='khsier', TAG='v1.2.3', RUNNER_TEMP=temporary)
                result = subprocess.run(['bash', '-e', '-o', 'pipefail', '-c', script],
                                        cwd=root, env=environment, capture_output=True, text=True)
                if current == base:
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertEqual(formula.read_text(), candidate)
                else:
                    self.assertNotEqual(result.returncode, 0)
                    self.assertEqual(formula.read_text(), current)

    def test_native_checks_install_the_generated_formula(self):
        workflow = WORKFLOW.read_text()
        validation = workflow.split('  brew-test:\n', 1)[1].split('  pull-request:\n', 1)[0]
        self.assertIn('os: [ubuntu-latest, macos-latest]', validation)
        self.assertIn('name: release-formula', validation)
        self.assertLess(validation.index('cp release-formula/candidate.rb'), validation.index('brew install'))
        self.assertIn('brew --repository zaubermaerchen/tap', validation)
        self.assertIn('brew test "zaubermaerchen/tap/$FORMULA"', validation)


if __name__ == '__main__':
    unittest.main()
