"""Independent checks for observation integrity, not a Claude host emulator."""
import importlib.util
import json
import os
from pathlib import Path
import tempfile
import subprocess
import sys
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('claude_probe', Path(__file__).with_name('probe.py'))
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)
inline_spec = importlib.util.spec_from_file_location('inline_probe', Path(__file__).with_name('inline_probe.py'))
inline_probe = importlib.util.module_from_spec(inline_spec)
inline_spec.loader.exec_module(inline_probe)


class ObservationIntegrityTests(unittest.TestCase):
    def test_ipc_auth_examples_are_removed_whole(self):
        for token in ["token:'FIXTURE-SECRET'", 'token:"FIXTURE-SECRET"', r'token:\"FIXTURE-SECRET\"']:
            with self.subTest(token=token):
                raw = "[uds-messaging] Inject messages: JSON.stringify({type:'auth'," + token + "})\n"
                self.assertEqual('[REDACTED: IPC authentication example]\n', probe.sanitize_text(raw))

    def test_jsonl_stays_parseable_with_nested_and_camel_case_credentials(self):
        raw = json.dumps({'event': 'SessionStart', 'accessToken': 'FIXTURE-SECRET',
                          'nested': {'client_secret': 'FIXTURE-SECRET'},
                          'stdout': json.dumps({'refresh_token': 'FIXTURE-SECRET', 'exit': 1})}) + '\n'
        result = probe.sanitize_text(raw)
        self.assertNotIn('FIXTURE-SECRET', result)
        parsed = json.loads(result)
        self.assertEqual('SessionStart', parsed['event'])
        self.assertEqual(1, json.loads(parsed['stdout'])['exit'])

    def test_diagnostics_identity_and_auth_status_survive(self):
        raw = {'apiKeySource': 'none', 'error': 'authentication_failed', 'exit': 1,
               'evaluator_archive_sha256': 'a' * 64, 'input_tokens': 123}
        self.assertEqual(raw, probe.sanitize_value(raw))

    def test_headers_private_keys_and_secret_cli_arguments_are_removed(self):
        raw = 'Authorization: Bearer FIXTURE-SECRET\n-----BEGIN PRIVATE KEY-----\nFIXTURE-SECRET\n-----END PRIVATE KEY-----\n'
        self.assertNotIn('FIXTURE-SECRET', probe.sanitize_text(raw))
        self.assertEqual(['tool', '--api-key', '[REDACTED]', '--check'],
                         probe.sanitize_value(['tool', '--api-key', 'FIXTURE-SECRET', '--check']))

    def test_public_debug_copy_redacts_before_write_and_preserves_local_source(self):
        with tempfile.TemporaryDirectory() as directory:
            source, destination = Path(directory) / 'local.log', Path(directory) / 'public.log'
            raw = "[uds-messaging] Inject messages: {token:'FIXTURE-SECRET'}\nexit=1\n"
            source.write_text(raw)
            probe.publish_capture(source, destination)
            self.assertEqual(raw, source.read_text())
            self.assertNotIn('FIXTURE-SECRET', destination.read_text())
            self.assertIn('exit=1', destination.read_text())

    def test_every_case_output_path_uses_sanitized_values(self):
        with tempfile.TemporaryDirectory() as directory:
            record = {'argv': ['tool', '--token', 'FIXTURE-SECRET'], 'exit': 1,
                      'stdout': "token='FIXTURE-SECRET'", 'stderr': 'Authorization: Bearer FIXTURE-SECRET'}
            probe.save_case(Path(directory), [record], 'expected',
                            {'event': 'SessionStart', 'authToken': 'FIXTURE-SECRET'}, 'unavailable')
            for path in Path(directory).iterdir():
                with self.subTest(path=path.name):
                    self.assertNotIn('FIXTURE-SECRET', path.read_text())
            self.assertEqual([1], json.loads((Path(directory) / 'observations.json').read_text())['exit_status'])

    def test_sanitizing_retained_evidence_again_is_idempotent(self):
        raw = json.dumps({'stdout': "[uds-messaging] Inject messages: {token:'FIXTURE-SECRET'}", 'exit': 0})
        once = probe.sanitize_text(raw)
        self.assertEqual(once, probe.sanitize_text(once))

    def test_zero_exit_without_host_event_is_not_delivery(self):
        self.assertEqual('incompatible', probe.classify_start({'exit': 0, 'timeout': False}, [], False))

    def test_wrong_event_cannot_substitute_for_startup(self):
        self.assertEqual('incompatible', probe.classify_start({'exit': 0, 'timeout': False},
                         [{'event': 'PreToolUse', 'handler_invoked': False}], False))

    def test_missing_interpreter_must_not_be_reported_invoked(self):
        self.assertEqual('fail', probe.classify_start({'exit': 0, 'timeout': False},
                         [{'event': 'SessionStart', 'handler_invoked': True}], False))

    def test_timeout_cannot_be_promoted_by_partial_output(self):
        self.assertEqual('incompatible', probe.classify_start({'exit': 0, 'timeout': True},
                         [{'event': 'SessionStart', 'handler_invoked': False}], False))

    def test_startup_observation_does_not_mean_production_support(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            probe.save_case(root, [], 'expected', {'startup': 'observed'}, 'unavailable')
            report = json.loads((root / 'observations.json').read_text())
            self.assertEqual('unavailable', report['conclusion'])
            self.assertEqual('unqualified', report['production_support'])

    def test_child_does_not_inherit_tokens_or_python_injection(self):
        with patch.dict(os.environ, {'ANTHROPIC_API_KEY': 'TEST-SENTINEL',
                        'CLAUDE_CODE_OAUTH_TOKEN': 'TEST-SENTINEL', 'PYTHONPATH': 'TEST-SENTINEL',
                        'SystemRoot': r'C:\Windows', 'PATH': 'TEST-SENTINEL'}):
            env = probe.child_environment(Path('isolated'))
        self.assertNotIn('TEST-SENTINEL', json.dumps(env))
        self.assertEqual('isolated', env['CLAUDE_CONFIG_DIR'])

    def test_sibling_prefix_is_not_contained(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / 'trial'
            self.assertFalse(probe.contained(Path(directory) / 'trial-other/python.exe', root))
            self.assertTrue(probe.contained(root / 'env/python.exe', root))

    def test_inventory_never_reads_secret_bytes(self):
        with tempfile.TemporaryDirectory() as directory:
            secret = Path(directory) / '.credentials.json'
            secret.write_text('TEST-SECRET-MUST-NOT-APPEAR')
            with patch.object(Path, 'read_bytes', side_effect=AssertionError('secret read')):
                result = probe.metadata([secret])
            self.assertTrue(result[str(secret)]['exists'])
            self.assertNotIn('TEST-SECRET', json.dumps(result))


@unittest.skipUnless(os.name == 'nt', 'Native PowerShell serialization boundary')
class NativeOutputBoundaryTests(unittest.TestCase):
    """Execute the shell guard with explicit test data, never a Claude host."""

    def run_guard(self, event='SessionStart', identity=None):
        with tempfile.TemporaryDirectory(prefix='claude guard test ') as directory:
            root = Path(directory)
            selected = str(root / 'missing/python.exe') if identity is None else sys.executable
            probe.dump(root / 'probe.json', {'interpreter': selected, 'event_log': str(root / 'events.jsonl')})
            if identity is not None:
                # A test stub validates protocol serialization, not real identity.
                (root / 'handler.py').write_text('print(' + repr(json.dumps(identity)) + ')', encoding='utf-8')
            env = dict(probe.child_environment(root / 'profile'), CLAUDE_PLUGIN_ROOT=str(root),
                       CLAUDE_PLUGIN_DATA=str(root / 'plugin data'))
            command = str(Path(os.environ['SystemRoot']) / 'System32/WindowsPowerShell/v1.0/powershell.exe')
            result = subprocess.run([command, '-NoProfile', '-NonInteractive', '-Command', inline_probe.INLINE],
                                    input=json.dumps({'hook_event_name': event, 'source': 'startup'}),
                                    capture_output=True, text=True, encoding='utf-8', env=env, timeout=30)
            self.assertEqual(0, result.returncode, result.stderr)
            return result.stdout, probe.events(root / 'events.jsonl')

    def test_missing_runtime_emits_only_documented_context_envelope(self):
        output, records = self.run_guard()
        parsed = json.loads(output)
        self.assertEqual({'hookSpecificOutput'}, set(parsed))
        self.assertEqual({'hookEventName', 'additionalContext'}, set(parsed['hookSpecificOutput']))
        self.assertEqual('SessionStart', parsed['hookSpecificOutput']['hookEventName'])
        self.assertIn('setup required', parsed['hookSpecificOutput']['additionalContext'])
        self.assertFalse(records[0]['handler_invoked'])

    def test_context_bytes_are_separate_from_identity_telemetry(self):
        context = 'Fixture governance: "quoted" line\nsecond line\n'
        output, records = self.run_guard(identity={'identity_exit': 0, 'identity': {'passed': True}, 'context': context})
        self.assertEqual(context, json.loads(output)['hookSpecificOutput']['additionalContext'])
        self.assertNotIn('identity_exit', json.loads(output))
        self.assertIn('identity_exit', json.loads(records[0]['handler_output']))

    def test_failed_identity_does_not_deliver_source_as_ready_context(self):
        output, _ = self.run_guard(identity={'identity_exit': 1, 'identity': {'passed': False}, 'context': 'DO NOT DELIVER'})
        self.assertNotIn('DO NOT DELIVER', output)
        self.assertIn('identity was not established', output)

    def test_tool_event_does_not_emit_an_allow_decision(self):
        output, records = self.run_guard(event='PreToolUse')
        self.assertEqual('', output)
        self.assertEqual('PreToolUse', records[0]['event'])
        self.assertNotIn('host_output', records[0])


if __name__ == '__main__':
    unittest.main()
