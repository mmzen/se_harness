"""Small setup, explicit-command and development-package acceptance."""
import importlib.util
import json
import os
import shutil
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
                for skill in ('setup', 'change', 'evidence', 'harness-orient'):
                    guidance = archive.read(f'verity-plane/skills/{skill}/SKILL.md')
                    self.assertEqual((ROOT/f'plugins/verity-plane/common/skills/{skill}/SKILL.md').read_bytes(), guidance)
                    self.assertIn(b'test', guidance)
                self.assertIn('verity-plane/hooks/hooks.json', names)
                for member in ('scripts/harness_runtime.py','scripts/activate.py','assets/bootstrap.md'):
                    self.assertEqual((ROOT/'plugins/verity-plane/common'/member).read_bytes(),
                                     archive.read('verity-plane/'+member))
                self.assertEqual((ROOT/'plugins/verity-plane/common/scripts/inject_instructions.py').read_bytes(),
                                 archive.read('verity-plane/scripts/inject_instructions.py'))
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

    def test_invalid_hooks_leave_an_existing_development_output_unchanged(self):
        source = self.base/'source'
        shutil.copytree(ROOT/'plugins/verity-plane', source/'plugins/verity-plane')
        output = self.base/'development'
        develop(source, self.wheel, output)
        before = {p.relative_to(output): p.read_bytes() for p in output.rglob('*') if p.is_file()}
        config = source/'plugins/verity-plane/codex/hooks/hooks.json'
        original = config.read_bytes()
        helper = source/'plugins/verity-plane/common/scripts/inject_instructions.py'
        helper_bytes = helper.read_bytes()
        invalid = [b'{', original.replace(b'SessionStart', b'PreToolUse'),
                   original.replace(b'--host codex', b'--host claude'),
                   original.replace(b'5000', b'0')]
        for raw in invalid:
            with self.subTest(raw=raw[:80]):
                config.write_bytes(raw)
                with self.assertRaises(AssemblyError):
                    develop(source, self.wheel, output)
                self.assertEqual(before, {p.relative_to(output): p.read_bytes() for p in output.rglob('*') if p.is_file()})
        config.write_bytes(original)
        helper.unlink()
        with self.assertRaisesRegex(AssemblyError, 'incomplete'):
            develop(source, self.wheel, output)
        self.assertEqual(before, {p.relative_to(output): p.read_bytes() for p in output.rglob('*') if p.is_file()})
        helper.write_bytes(helper_bytes)
        activation = source/'plugins/verity-plane/common/scripts/activate.py'
        activation.unlink()
        with self.assertRaisesRegex(AssemblyError, 'incomplete'):
            develop(source, self.wheel, output)
        self.assertEqual(before, {p.relative_to(output): p.read_bytes() for p in output.rglob('*') if p.is_file()})

    def test_development_wrapper_packages_both_host_hooks(self):
        output = self.base/'wrapper'
        result = subprocess.run([sys.executable, str(ROOT/'scripts/build_plugin_archives.py'), 'develop',
                                 '--wheel', str(self.wheel), '--output-directory', str(output)],
                                cwd=ROOT, capture_output=True)
        self.assertEqual(0, result.returncode, result.stderr.decode(errors='replace'))
        for host in ('codex', 'claude'):
            with zipfile.ZipFile(output/f'verity-plane-{host}.zip') as archive:
                self.assertIn('verity-plane/hooks/hooks.json', archive.namelist())

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

    def test_setup_reuses_an_immutable_environment_and_preserves_checker_result(self):
        data = self.base/'private'
        calls=[]
        identity={'version':'0.0.0','archive_name':self.wheel.name,
                  'archive_sha256':setup.hashlib.sha256(self.wheel.read_bytes()).hexdigest()}
        def run(argv, **kwargs):
            calls.append(argv)
            if 'venv' in argv: Path(argv[-1]).mkdir(parents=True)
            return subprocess.CompletedProcess(argv, 7 if 'doctor' in argv else 0)
        with patch.object(setup.subprocess, 'run', side_effect=run), patch.object(setup,'query_identity',return_value=identity):
            for _ in range(2):
                self.assertEqual(7, setup.setup(self.target, data, self.wheel))
        self.assertEqual(1, sum('venv' in argv for argv in calls))
        self.assertEqual(1, sum('pip' in argv for argv in calls))
        self.assertIn('--no-index', calls[1])
        self.assertNotIn('--force-reinstall', calls[1])
        self.assertEqual(2, sum('doctor' in argv for argv in calls))
        self.assertEqual([], list(self.target.iterdir()))

    def test_setup_rejects_private_environment_in_the_checkout(self):
        with self.assertRaisesRegex(ValueError, 'outside the repository'):
            setup.setup(self.target, self.target/'private', self.wheel)
        self.assertFalse((self.target/'private').exists())

    def test_setup_refuses_contention_and_partial_environment_without_running_code(self):
        identity={'version':'0.0.0','archive_sha256':setup.hashlib.sha256(self.wheel.read_bytes()).hexdigest()}
        environment=setup.environment_path(self.base/'private',identity)
        lock=environment.with_name(environment.name+'.lock')
        with patch.object(setup.subprocess,'run') as command:
            with setup.exclusive(lock):
                with self.assertRaisesRegex(ValueError,'another operation'):
                    setup.setup(self.target,self.base/'private',self.wheel)
            environment.mkdir()
            (environment/'partial').write_text('retained failure')
            with self.assertRaisesRegex(ValueError,'incomplete private environment'):
                setup.setup(self.target,self.base/'private',self.wheel)
            command.assert_not_called()
        self.assertEqual('retained failure',(environment/'partial').read_text())

    def test_setup_rejects_same_version_wheel_substitution_before_writes(self):
        (self.target/'.engineering-harness.toml').write_text('[harness]\ntool_version="0.0.0"\n')
        (self.target/'.engineering-harness.lock').write_text(json.dumps({'schema':4,'tool_version':'0.0.0',
            'evaluator':{'version':'0.0.0','archive_sha256':'f'*64}}))
        with patch.object(setup.subprocess,'run') as command:
            with self.assertRaisesRegex(ValueError,'does not match'):
                setup.setup(self.target,self.base/'private',self.wheel)
            command.assert_not_called()
        self.assertFalse((self.base/'private').exists())

    def test_setup_reports_missing_python_prerequisite_before_writes(self):
        with patch.dict(sys.modules, {'ensurepip': None}):
            with self.assertRaises(ImportError):
                setup.setup(self.target, self.base/'private', self.wheel)
        self.assertFalse((self.base/'private').exists())

    @unittest.skipUnless(os.environ.get('SE_HARNESS_TEST_PLUGIN_WHEEL'), 'real local wheel supplied in installed acceptance')
    def test_real_setup_create_reuse_and_repair(self):
        wheel = Path(os.environ['SE_HARNESS_TEST_PLUGIN_WHEEL']).resolve()
        python = os.environ.get('SE_HARNESS_TEST_PLUGIN_PYTHON', sys.executable)
        subprocess.run([python, '-I', '-m', 'se_harness', 'init', str(self.target), '--project-name', 'Plugin fixture', '--integration', 'git'], check=True,
                       cwd=self.base, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        argv = [python, '-I', str(SETUP), '--target', str(self.target), '--data-root', str(self.base/'private'), '--wheel', str(wheel)]
        for attempt in range(2):
            result = subprocess.run(argv, cwd=self.base, capture_output=True)
            self.assertEqual(0, result.returncode, result.stdout.decode(errors='replace')+result.stderr.decode(errors='replace'))
            if attempt == 1:
                environment = setup.environment_path(self.base/'private', {'version':setup.re.fullmatch(r'se_harness-(.+)-py3-none-any.whl',wheel.name)[1], 'archive_sha256':setup.hashlib.sha256(wheel.read_bytes()).hexdigest()})
                package = next(environment.glob('Lib/site-packages/se_harness/__init__.py'), None)
                if package is None:
                    package = next(environment.glob('lib/python*/site-packages/se_harness/__init__.py'))
                original = package.read_bytes()
                package.unlink()  # Never repair over a potentially active environment.
                refused = subprocess.run(argv, cwd=self.base, capture_output=True)
                self.assertNotEqual(0, refused.returncode)
                self.assertFalse(package.exists())
                package.write_bytes(original)
        managed = self.target/'.gitattributes'
        self.assertTrue(managed.is_file())
        managed.write_text('changed managed content')
        failed = subprocess.run(argv, cwd=self.base, capture_output=True)
        self.assertNotEqual(0, failed.returncode)
        self.assertIn(b'.gitattributes', failed.stdout)


if __name__ == '__main__':
    unittest.main()
