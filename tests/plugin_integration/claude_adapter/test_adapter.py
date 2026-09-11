import copy
import json
from pathlib import Path
import tempfile
import unittest

import support as s


class BindingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory(prefix='claude-adapter-')
        cls.f = s.create_fixture(Path(cls.temp.name) / 'case')

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def setUp(self):
        s.dump(self.f['config_path'], self.f['config'])

    def test_native_hooks_match_inline_source_and_are_synchronous(self):
        source = (s.ADAPTER / 'hooks/guard.txt').read_text()
        self.assertEqual(json.loads((s.ADAPTER / 'hooks/hooks.json').read_text()), s.binding.hooks(source))
        self.assertNotIn('-ExecutionPolicy', source)
        self.assertNotIn('Invoke-Expression', source)

    def test_real_session_uses_absolute_isolated_python_and_full_context(self):
        result = s.direct(self.f, s.event(self.f))
        record = s.guard_record(result)
        self.assertEqual(record.get('status'), 'shared-response', result['stderr'])
        self.assertEqual(record['argv'][:3], [str(s.PYTHON), '-I', '-B'])
        self.assertTrue(Path(record['argv'][3]).is_absolute())
        context = s.response(result)['additionalContext']
        self.assertIn('END VERIFIED GOVERNANCE', context)
        self.assertIn((self.f['repo'] / 'ENGINEERING_HARNESS.md').read_text(), context)

    def test_real_scope_refusal_and_permitted_edit(self):
        yes = s.direct(self.f, s.event(self.f, 'PreToolUse'))
        no = s.direct(self.f, s.event(self.f, 'PreToolUse', path='outside-scope.txt'))
        self.assertFalse(s.denied(yes), yes['stderr'])
        self.assertTrue(s.denied(no), no['stderr'])
        self.assertNotIn('permissionDecision', s.response(yes))

    def test_missing_runtime_never_launches_python(self):
        config = dict(self.f['config'], environment=str(self.f['space'] / 'not installed'))
        s.dump(self.f['config_path'], config)
        result = s.direct(self.f, s.event(self.f))
        self.assertFalse(s.guard_record(result)['interpreter_invoked'])
        self.assertIn('SETUP REQUIRED', result['stdout'])

    def test_malformed_and_missing_tool_fields_deny(self):
        self.assertTrue(s.denied(s.direct(self.f, b'{bad', kind='PreToolUse')))
        for field in ('tool_input', 'tool_name', 'hook_event_name'):
            event = s.event(self.f, 'PreToolUse')
            del event[field]
            self.assertTrue(s.denied(s.direct(self.f, event, kind='PreToolUse')))

    def test_unsupported_tools_leave_setup_access_without_allow(self):
        event = s.event(self.f, 'PreToolUse', tool='Bash')
        result = s.direct(self.f, event)
        self.assertIn('COVERAGE GAP', result['stdout'])
        self.assertFalse(s.guard_record(result)['interpreter_invoked'])
        self.assertNotIn('permissionDecision', s.response(result))

    def test_event_quotes_and_unicode_survive_exactly(self):
        event = s.event(self.f, 'PreToolUse')
        event['tool_input']['content'] = 'quoted "text" café \\ value\n'
        path = self.f['plugin'] / 'scripts/check-tool-action.py'
        original = path.read_bytes()
        try:
            path.write_text('import sys,json\nraw=sys.stdin.buffer.read()\nprint(json.dumps({"hookSpecificOutput":{"hookEventName":"PreToolUse","additionalContext":json.dumps({"argv":sys.argv,"received":raw.decode("utf8")})}}))\n', encoding='utf8')
            result = s.direct(self.f, event)
            self.assertFalse(s.denied(result), result['stderr'])
            observed = json.loads(s.response(result)['additionalContext'])
            self.assertEqual(json.loads(observed['received']), event)
            self.assertEqual(observed['argv'][0], str(path))
            self.assertEqual(observed['argv'][observed['argv'].index('--repo') + 1], str(self.f['repo']))
        finally:
            path.write_bytes(original)

    def test_unexpected_output_controls_are_refused(self):
        path = self.f['plugin'] / 'scripts/check-tool-action.py'
        original = path.read_bytes()
        try:
            for value in ({'hookSpecificOutput': {'hookEventName': 'PreToolUse', 'additionalContext': 'ok', 'permissionDecision': 'allow'}},
                          {'hookSpecificOutput': {'hookEventName': 'PreToolUse', 'additionalContext': 'ok'}, 'continue': True}):
                path.write_text('print(' + repr(json.dumps(value)) + ')\n', encoding='utf8')
                self.assertTrue(s.denied(s.direct(self.f, s.event(self.f, 'PreToolUse'))))
        finally:
            path.write_bytes(original)

    def test_profile_and_loaded_binding_cannot_self_qualify(self):
        loaded = json.loads((s.ADAPTER / 'hooks/hooks.json').read_text())
        observed = {'host': '2.1.266', 'os': 'Windows', 'python': '3.14.6', 'evaluator': '0.16.0'}
        answer = s.binding.assess_binding(self.f['config'], loaded, observed, s.binding.PROFILE['decision'])
        self.assertTrue(answer['eligible_for_live_assessment'])
        self.assertFalse(answer['qualified'])
        for wrong in ('Linux', 'Windows-new'):
            self.assertFalse(s.binding.assess_binding(self.f['config'], loaded, dict(observed, os=wrong), s.binding.PROFILE['decision'])['eligible_for_live_assessment'])
        self.assertFalse(s.binding.assess_binding(self.f['config'], loaded, observed, 'exclude-claude')['eligible_for_live_assessment'])
        for field, value in [('async', True), ('timeout', 2)]:
            modified = copy.deepcopy(loaded)
            modified['hooks']['PreToolUse'][0]['hooks'][0][field] = value
            self.assertFalse(s.binding.assess_binding(self.f['config'], modified, observed, s.binding.PROFILE['decision'])['eligible_for_live_assessment'])


if __name__ == '__main__':
    unittest.main()
