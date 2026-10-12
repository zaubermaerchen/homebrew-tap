"""Select Formula checks targets; print a JSON array for the workflow matrix."""
import json
import os
from pathlib import Path
import re
import subprocess
import sys


def select_formulae(root, event, formula='', base='', head=''):
    available = sorted(path.stem for path in (root / 'Formula').glob('*.rb') if path.is_file())
    if event == 'workflow_dispatch' and formula:
        if formula not in available:
            raise ValueError(f'Unknown formula: {formula!r}. Available: {", ".join(available)}')
        return [formula]
    if event != 'pull_request':
        return available
    try:
        if not all(re.fullmatch(r'[0-9a-f]{40}', ref) for ref in (base, head)):
            raise ValueError('Missing or invalid PR commit SHA')
        diff = subprocess.run(
            ['git', 'diff', '--name-only', '-z', '--no-renames', f'{base}...{head}', '--'],
            cwd=root, check=True, capture_output=True,
        ).stdout.decode('utf-8')
        if diff and not diff.endswith('\0'):
            raise ValueError('Unexpected git diff output')
        changed = diff.split('\0')[:-1]
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        print(f'Cannot detect PR changes; checking all formulae: {error}', file=sys.stderr)
        return available

    selected = set()
    for name in changed:
        path = Path(name)
        if path.parent == Path('Formula') and path.suffix == '.rb':
            if path.stem in available:
                selected.add(path.stem)
        elif name not in ('README.md', 'LICENSE') and not name.startswith('docs/'):
            return available
    return sorted(selected)


if __name__ == '__main__':
    try:
        selected = select_formulae(
            Path.cwd(), os.environ['GITHUB_EVENT_NAME'], os.environ.get('FORMULA', ''),
            os.environ.get('PR_BASE_SHA', ''), os.environ.get('PR_HEAD_SHA', ''),
        )
    except ValueError as error:
        sys.exit(str(error))
    print(json.dumps(selected))
