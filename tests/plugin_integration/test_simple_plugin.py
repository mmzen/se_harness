"""Small setup, explicit-command and development-package acceptance."""
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from repository_tools.plugin_distribution import AssemblyError, develop

SETUP = ROOT / 'plugins/verity-plane/common/scripts/setup.py'
spec = importlib.util.spec_from_file_location('plugin_setup', SETUP)
setup = importlib.util.module_from_spec(spec)
spec.loader.exec_module(setup)


class SimplePluginTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix='simple-plugin-')
        self.addCleanup(temporary.cleanup)
        self.base = Path(temporary.name).resolve()
        self.target = self.base/'repository'
        self.target.mkdir()
        self.wheel = self.base/'se_harness-0.0.0-py3-none-any.whl'
        with zipfile.ZipFile(self.wheel, 'w') as archive:
            archive.writestr('se_harness-0.0.0.dist-info/METADATA', 'Metadata-Version: 2.1\nName: se-harness\nVersion: 0.0.0\n')

    def test_development_build_uses_current_source_and_replaces_only_its_output(self):
        output = self.base/'development'
        result = develop(ROOT, self.wheel, output)
        self.assertFalse(result['promotable'])
        for host in ('codex','claude'):
            with zipfile.ZipFile(output/f'verity-plane-{host}.zip') as archive:
                names = archive.namelist()
                self.assertIn('verity-plane/DEVELOPMENT.md', names)
                self.assertIn('verity-plane/packages/'+self.wheel.name, names)
                self.assertEqual((ROOT/'plugins/verity-plane/common/skills/change/SKILL.md').read_bytes(),
                                 archive.read('verity-plane/skills/change/SKILL.md'))
                self.assertFalse(any('/hooks/' in name for name in names))
                manifest = '.codex-plugin' if host == 'codex' else '.claude-plugin'
                self.assertNotIn('hooks', json.loads(archive.read(f'verity-plane/{manifest}/plugin.json')))
        (output/'old-build-file').write_text('obsolete')
        develop(ROOT, self.wheel, output)
        self.assertFalse((output/'old-build-file').exists())
        unrelated = self.base/'unrelated'
        unrelated.mkdir()
        (unrelated/'keep').write_text('user content')
        with self.assertRaisesRegex(AssemblyError, 'not owned'):
            develop(ROOT, self.wheel, unrelated)
        self.assertEqual('user content', (unrelated/'keep').read_text())

    def test_development_archive_cannot_use_the_release_check_without_release_inputs(self):
        result = subprocess.run([sys.executable, str(ROOT/'scripts/build_plugin_archives.py'), 'check',
                                 '--wheel', str(self.wheel), '--output-directory', str(self.base/'output')],
                                capture_output=True)
        self.assertNotEqual(0, result.returncode)
        self.assertIn(b'release build/check requires', result.stderr)

    def test_development_build_accepts_windows_wheel_metadata(self):
        with zipfile.ZipFile(self.wheel, 'w') as archive:
            archive.writestr('se_harness-0.0.0.dist-info/METADATA',
                             b'Metadata-Version: 2.1\r\nName: se-harness\r\nVersion: 0.0.0\r\n')
        output = self.base/'windows-wheel'
        result = develop(ROOT, self.wheel, output)
        self.assertFalse(result['promotable'])
        with zipfile.ZipFile(output/'verity-plane-codex.zip') as archive:
            self.assertEqual(self.wheel.read_bytes(), archive.read('verity-plane/packages/'+self.wheel.name))

    def test_setup_retries_the_same_environment_and_preserves_the_checker_result(self):
        data = self.base/'private'
        calls=[]
        def run(argv, **kwargs):
            calls.append(argv)
            return subprocess.CompletedProcess(argv, 7 if 'doctor' in argv else 0)
        with patch.object(setup.subprocess, 'run', side_effect=run):
            for _ in range(2):
                self.assertEqual(7, setup.setup(self.target, data, self.wheel))
        self.assertEqual(calls[0], calls[3])
        self.assertIn('--force-reinstall', calls[1])
        self.assertIn('--no-index', calls[1])
        self.assertIn('--no-deps', calls[1])
        self.assertEqual(2, sum('doctor' in argv for argv in calls))
        self.assertEqual([], list(self.target.iterdir()))

    def test_setup_rejects_private_environment_in_the_checkout(self):
        with self.assertRaisesRegex(ValueError, 'outside the repository'):
            setup.setup(self.target, self.target/'private', self.wheel)
        self.assertFalse((self.target/'private').exists())

    def test_setup_reports_missing_python_prerequisite_before_writes(self):
        with patch.dict(sys.modules, {'ensurepip': None}):
            with self.assertRaises(ImportError):
                setup.setup(self.target, self.base/'private', self.wheel)
        self.assertFalse((self.base/'private').exists())

    @unittest.skipUnless(os.environ.get('SE_HARNESS_TEST_PLUGIN_WHEEL'), 'real local wheel supplied in installed acceptance')
    def test_real_setup_create_reuse_and_repair(self):
        wheel = Path(os.environ['SE_HARNESS_TEST_PLUGIN_WHEEL']).resolve()
        python = os.environ.get('SE_HARNESS_TEST_PLUGIN_PYTHON', sys.executable)
        subprocess.run([python, '-I', '-m', 'se_harness', 'init', str(self.target), '--project-name', 'Plugin fixture'], check=True,
                       cwd=self.base, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        argv = [python, '-I', str(SETUP), '--target', str(self.target), '--data-root', str(self.base/'private'), '--wheel', str(wheel)]
        for attempt in range(3):
            result = subprocess.run(argv, cwd=self.base, capture_output=True)
            self.assertEqual(0, result.returncode, result.stdout.decode(errors='replace')+result.stderr.decode(errors='replace'))
            if attempt == 1:
                environment = self.base/'private/verity-plane/evaluator'
                package = next(environment.glob('Lib/site-packages/se_harness/__init__.py'), None)
                if package is None:
                    package = next(environment.glob('lib/python*/site-packages/se_harness/__init__.py'))
                package.unlink()  # Interrupted installation; the next setup must repair it.
        (self.target/'ENGINEERING_HARNESS.md').write_text('changed managed content')
        failed = subprocess.run(argv, cwd=self.base, capture_output=True)
        self.assertNotEqual(0, failed.returncode)
        self.assertIn(b'ENGINEERING_HARNESS.md', failed.stdout)


if __name__ == '__main__':
    unittest.main()
