"""Require the complete product diff to be exactly the proposed read loop."""
import os
from pathlib import Path
import subprocess

baseline = os.environ['RAMDISK_BASELINE_COMMIT']
paths = subprocess.check_output(['git', 'diff', '--name-only', baseline, 'HEAD', '--',
    'se_harness', 'tests', 'templates', 'repository_tools', 'scripts', 'pyproject.toml'], text=True).splitlines()
assert paths == ['se_harness/skill_ownership.py'], paths
before = subprocess.check_output(['git', 'show', baseline + ':se_harness/skill_ownership.py'], text=True)
after = Path('se_harness/skill_ownership.py').read_text(encoding='utf-8')
old = '            raw = handle.read(limit + 1)\n'
new = '''            chunks = []
            remaining = limit + 1
            while remaining:
                chunk = handle.read(min(64 * 1024, remaining))
                if not chunk:
                    break
                chunks.append(chunk)
                remaining -= len(chunk)
            raw = b"".join(chunks)
'''
assert before.count(old) == 1
assert before.replace(old, new) == after, 'Unexpected change beyond bounded reads'
print('READER_DIFF_OK: only the bounded read loop changed; all guards and test cases unchanged')
