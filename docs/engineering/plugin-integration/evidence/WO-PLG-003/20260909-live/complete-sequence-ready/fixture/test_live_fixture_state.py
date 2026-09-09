from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import live_fixture_state


class PreparationBoundaryTests(unittest.TestCase):
    def test_substituted_wheel_refused_before_any_command_or_fixture_write(self):
        with tempfile.TemporaryDirectory(prefix='codex-wheel-refusal-') as folder:
            wheel = Path(folder) / 'se_harness-0.16.0-py3-none-any.whl'
            wheel.write_bytes(b'not the selected released wheel')
            args = ['live_fixture_state.py', '--sandbox', str(Path(folder) / 'untouched'),
                    '--action', 'prepare', '--evidence-name', 'must-not-exist', '--wheel', str(wheel)]
            with patch.object(sys, 'argv', args), patch.object(live_fixture_state, 'run') as execute:
                with self.assertRaises(SystemExit) as raised:
                    live_fixture_state.main()
                self.assertEqual(raised.exception.code, 2)
                execute.assert_not_called()
            self.assertFalse((Path(folder) / 'untouched').exists())


if __name__ == '__main__':
    unittest.main()
