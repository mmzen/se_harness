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
live_spec = importlib.util.spec_from_file_location('live_sessions', Path(__file__).with_name('live_sessions.py'))
live_sessions = importlib.util.module_from_spec(live_spec)
live_spec.loader.exec_module(live_sessions)
tool_spec = importlib.util.spec_from_file_location('tool_setup', Path(__file__).with_name('tool_setup.py'))
tool_setup = importlib.util.module_from_spec(tool_spec)
tool_spec.loader.exec_module(tool_setup)
denial_spec = importlib.util.spec_from_file_location('denial_probe', Path(__file__).with_name('denial_probe.py'))
denial_probe = importlib.util.module_from_spec(denial_spec)
denial_spec.loader.exec_module(denial_probe)


class ObservationIntegrityTests(unittest.TestCase):
    def test_provider_error_cannot_be_promoted_by_success_subtype(self):
        record = {'exit': 0, 'timeout': False, 'stdout': json.dumps({'type': 'result', 'subtype': 'success', 'is_error': True})}
        self.assertFalse(live_sessions.completed_successfully(record))

    def test_ready_requires_this_invocations_event_and_matching_context_receipt(self):
        record = {'exit': 0, 'timeout': False, 'stdout': json.dumps({'type': 'result', 'subtype': 'success', 'is_error': False})}
        event = {'event': 'SessionStart', 'handler_exit': 0,
                 'handler_output': json.dumps({'governance_readiness': True, 'context': 'fresh'}),
                 'host_output': {'hookSpecificOutput': {'additionalContext': 'fresh'}}}
        receipt = 'Hook SessionStart (fixture) provided additionalContext (5 chars)'
        self.assertTrue(tool_setup.ready_context_observed(record, [event], receipt))
        self.assertFalse(tool_setup.ready_context_observed(record, [], receipt))
        self.assertFalse(tool_setup.ready_context_observed(record, [event], receipt.replace('(5 chars)', '(4 chars)')))
        event['host_output']['hookSpecificOutput']['additionalContext'] = 'stale'
        self.assertFalse(tool_setup.ready_context_observed(record, [event], receipt))

    def test_empty_or_failed_handler_is_unready_without_crashing(self):
        for event in [{}, {'handler_exit': 1, 'handler_output': ''},
                      {'handler_exit': 0, 'handler_output': 'invalid'},
                      {'handler_exit': 0, 'handler_output': 'null'}]:
            self.assertFalse(tool_setup.handler_readiness(event))

    def test_ready_requires_successful_handler_and_boolean_true(self):
        self.assertTrue(tool_setup.handler_readiness({'handler_exit': 0, 'handler_output': '{"governance_readiness":true}'}))
        self.assertFalse(tool_setup.handler_readiness({'handler_exit': 1, 'handler_output': '{"governance_readiness":true}'}))
        self.assertFalse(tool_setup.handler_readiness({'handler_exit': 0, 'handler_output': '{"governance_readiness":"true"}'}))

    def denial_fixture(self):
        target = str(Path('sentinel.txt').resolve())
        records = [
            {'type': 'assistant', 'message': {'content': [{'type': 'tool_use', 'id': 'write-1', 'name': 'Write', 'input': {'file_path': target}}]}},
            {'type': 'user', 'message': {'content': [{'type': 'tool_result', 'tool_use_id': 'write-1', 'is_error': True, 'content': denial_probe.REASON}]}},
            {'type': 'result', 'subtype': 'success', 'is_error': False}]
        command = {'exit': 0, 'timeout': False, 'stdout': '\n'.join(json.dumps(r) for r in records)}
        events = [{'host_output': {'hookSpecificOutput': {'permissionDecision': 'deny', 'permissionDecisionReason': denial_probe.REASON}}}]
        return target, command, events, records

    def test_exact_correlated_tool_refusal_is_observed(self):
        target, command, events, _ = self.denial_fixture()
        self.assertTrue(denial_probe.denial_observed(command, events, target, True))

    def test_model_only_denial_phrase_is_not_a_host_refusal(self):
        target, command, events, records = self.denial_fixture()
        records[1] = {'type': 'assistant', 'message': {'content': [{'type': 'text', 'text': denial_probe.REASON}]}}
        command['stdout'] = '\n'.join(json.dumps(r) for r in records)
        self.assertFalse(denial_probe.denial_observed(command, events, target, True))

    def test_partial_timeout_does_not_pass_despite_refusal_records(self):
        target, command, events, _ = self.denial_fixture()
        command['timeout'] = True
        self.assertFalse(denial_probe.denial_observed(command, events, target, True))
    def test_model_prose_cannot_substitute_for_structured_host_result(self):
        record = {'stdout': '[]\nnull\nnot JSON\n' + json.dumps({'type': 'assistant', 'message': 'The tool succeeded.'})}
        self.assertEqual({}, live_sessions.result_message(record))

    def test_actual_error_result_is_preserved_even_with_success_subtype(self):
        result = {'type': 'result', 'subtype': 'success', 'is_error': True, 'result': 'provider refused'}
        self.assertEqual(result, live_sessions.result_message({'stdout': json.dumps(result)}))
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

    def test_sentinel_denial_is_exact_after_path_separator_normalization(self):
        with tempfile.TemporaryDirectory(prefix='claude sentinel test ') as directory:
            root = Path(directory)
            target = root / 'governed-target.txt'
            probe.dump(root / 'probe.json', {'interpreter': str(root / 'missing.exe'),
                       'event_log': str(root / 'events.jsonl'), 'sentinel': str(target)})
            env = dict(probe.child_environment(root / 'profile'), CLAUDE_PLUGIN_ROOT=str(root))
            command = str(Path(os.environ['SystemRoot']) / 'System32/WindowsPowerShell/v1.0/powershell.exe')
            hook = inline_probe.INLINE.replace('[IO.File]::AppendAllText', tool_setup.SENTINEL + '[IO.File]::AppendAllText', 1)
            for tool, path, expected in [('Write', target.as_posix(), 'deny'),
                                         ('Write', str(root / 'other.txt'), None),
                                         ('Read', str(target), None)]:
                with self.subTest(tool=tool, path=path):
                    result = subprocess.run([command, '-NoProfile', '-NonInteractive', '-Command', hook],
                        input=json.dumps({'hook_event_name': 'PreToolUse', 'tool_name': tool, 'tool_input': {'file_path': path}}),
                        capture_output=True, text=True, encoding='utf-8', env=env, timeout=30)
                    self.assertEqual(0, result.returncode, result.stderr)
                    if expected:
                        self.assertEqual(expected, json.loads(result.stdout)['hookSpecificOutput']['permissionDecision'])
                    else:
                        self.assertEqual('', result.stdout)


if __name__ == '__main__':
    unittest.main()
