"""One-shot responses for exact commands already reviewed for this test.

This is probe-client orchestration, not a production authority evaluator.
Never returns a persistent permission or policy amendment.
"""
from pathlib import Path


def exact_setup_decision(message, *, cwd, shell, reviewed_commands, reviewed_reads=None):
    if message.get('method') != 'item/commandExecution/requestApproval':
        return None
    params = message.get('params', {})
    if params.get('kind') != 'command' or params.get('cwd') != str(cwd):
        return 'cancel'
    if 'accept' not in params.get('availableDecisions', []):
        return 'cancel'
    for command in reviewed_commands:
        expected = f'"{shell}" -Command "{command}"'
        # The host formats the Windows display command with doubled separators.
        # Only that display escaping is normalized; all syntax remains exact.
        actual = params.get('command', '').replace('\\\\', '\\')
        if actual == expected and params.get('commandActions') == [{'type': 'unknown', 'command': command}]:
            return 'accept'
    for command, path in (reviewed_reads or {}).items():
        expected = f'"{shell}" -Command "{command}"'
        actual = params.get('command', '').replace('\\\\', '\\')
        actions = [{'type': 'read', 'command': command, 'name': Path(path).name, 'path': str(path)}]
        if actual == expected and params.get('commandActions') == actions:
            return 'accept'
    return 'cancel'
