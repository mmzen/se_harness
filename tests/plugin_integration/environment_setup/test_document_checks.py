"""Fast negative checks execute the reference's code, not a copied algorithm."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from run_acceptance import snippets


class DocumentChecks(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix='plugin setup checks ')
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.blocks = snippets()

    def run_block(self, name, *args):
        return subprocess.run([sys.executable, '-I', '-S', '-c', self.blocks[name], *map(str, args)],
                              capture_output=True, text=True)

    def test_archive_observation_is_required_even_with_expected_flag(self):
        path = self.root / 'identity.json'
        valid = {'schema': 'se-harness-runtime-identity-v3', 'passed': True, 'harness_version': '0.16.0',
                 'evaluator_payload_sha256': 'a' * 64, 'evaluator_archive_sha256': 'b' * 64,
                 'evaluator_wheel_sha256': 'b' * 64}
        path.write_text(json.dumps(valid), encoding='utf8')
        self.assertEqual(self.run_block('accept', path, '0.16.0', 'a' * 64, 'b' * 64).returncode, 0)
        for field, value in [('passed', False), ('evaluator_archive_sha256', None),
                             ('evaluator_archive_sha256', 'c' * 64), ('harness_version', '0.17.0'),
                             ('evaluator_payload_sha256', 'c' * 64)]:
            with self.subTest(field=field, value=value):
                path.write_text(json.dumps({**valid, field: value}), encoding='utf8')
                self.assertNotEqual(self.run_block('accept', path, '0.16.0', 'a' * 64, 'b' * 64).returncode, 0)

    def test_partial_or_malformed_identity_does_not_become_ready(self):
        path = self.root / 'identity.json'
        for content in ('', '{', '{}', 'null', '{"passed": true}'):
            with self.subTest(content=content):
                path.write_text(content, encoding='utf8')
                self.assertNotEqual(self.run_block('accept', path, '0.16.0', 'a' * 64, 'b' * 64).returncode, 0)

    def test_entry_point_text_does_not_prove_installed_files(self):
        env = self.root / 'absent environment'
        folder = env / ('Scripts' if os.name == 'nt' else 'bin')
        python = folder / ('python.exe' if os.name == 'nt' else 'python')
        entry = folder / ('harnessctl.exe' if os.name == 'nt' else 'harnessctl')
        self.assertNotEqual(self.run_block('entry', env, python, entry).returncode, 0)
        self.assertFalse(env.exists())

    def test_environment_cannot_be_created_inside_target(self):
        repo = self.root / 'repository'
        data = repo / 'plugin data'
        data.mkdir(parents=True)
        wheel = self.root / 'se_harness-0.16.0-py3-none-any.whl'
        wheel.write_bytes(b'not installed')
        env = data / 'environment'
        result = self.run_block('inputs', repo, data, env, wheel, '0.16.0', 'a' * 64, 'b' * 64, data / 'identity.json')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('separate from the repository', result.stderr)
        self.assertFalse(env.exists())


if __name__ == '__main__':
    unittest.main()
