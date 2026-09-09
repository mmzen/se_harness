import copy
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from review_approval import exact_setup_decision


class ApprovalBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.cwd = r'C:\fixture with spaces\repo'
        self.shell = r'C:\Windows\powershell.exe'
        self.command = "& 'C:\\provided\\python.exe' -I -m venv 'C:\\fixture with spaces\\env'"
        rendered = f'"{self.shell}" -Command "{self.command}"'.replace('\\', '\\\\')
        self.message = {'id': 1, 'method': 'item/commandExecution/requestApproval', 'params': {
            'kind': 'command', 'cwd': self.cwd, 'command': rendered,
            'commandActions': [{'type': 'unknown', 'command': self.command}],
            'availableDecisions': ['accept', 'cancel']}}

    def decide(self, value):
        return exact_setup_decision(value, cwd=self.cwd, shell=self.shell, reviewed_commands=[self.command])

    def test_exact_reviewed_command_gets_one_shot_only(self):
        self.assertEqual(self.decide(self.message), 'accept')

    def test_outer_command_cannot_append_an_action(self):
        changed = copy.deepcopy(self.message)
        changed['params']['command'] += ' & destructive-command'
        self.assertEqual(self.decide(changed), 'cancel')

    def test_same_inner_command_with_different_cwd_is_refused(self):
        changed = copy.deepcopy(self.message)
        changed['params']['cwd'] = r'C:\unrelated'
        self.assertEqual(self.decide(changed), 'cancel')

    def test_different_action_or_missing_one_shot_choice_is_refused(self):
        for key, value in [('commandActions', []), ('availableDecisions', ['acceptWithExecpolicyAmendment'])]:
            changed = copy.deepcopy(self.message)
            changed['params'][key] = value
            self.assertEqual(self.decide(changed), 'cancel')

    def test_unrelated_request_has_no_fabricated_response(self):
        self.assertIsNone(self.decide({'method': 'item/permissions/requestApproval', 'params': {}}))

    def test_exact_named_skill_read_only(self):
        path = Path(r'C:\fixture\plugins\setup\SKILL.md')
        command = "Get-Content -LiteralPath 'C:/fixture/plugins/setup/SKILL.md'"
        message = copy.deepcopy(self.message)
        message['params']['command'] = f'"{self.shell}" -Command "{command}"'
        message['params']['commandActions'] = [{'type': 'read', 'command': command,
                                               'name': path.name, 'path': str(path)}]
        arguments = dict(cwd=self.cwd, shell=self.shell, reviewed_commands=[], reviewed_reads={command: path})
        self.assertEqual(exact_setup_decision(message, **arguments), 'accept')
        message['params']['commandActions'][0]['path'] = r'C:\unrelated\credentials'
        self.assertEqual(exact_setup_decision(message, **arguments), 'cancel')


if __name__ == '__main__':
    unittest.main()
