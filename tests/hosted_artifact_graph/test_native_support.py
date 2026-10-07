"""Boundaries of the one-call native qualification helper."""
import argparse
import tempfile
import unittest
from pathlib import Path

from native_call import contained, remote_argv


class NativeCallBoundaries(unittest.TestCase):
    def test_path_escape_and_existing_export_refuse(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            with self.assertRaises(ValueError):contained(root,'../outside.json')
            (root/'export').mkdir()
            with self.assertRaises(ValueError):contained(root,'export',new=True)

    def test_endpoint_cannot_leave_loopback(self):
        config={'endpoint':'https://example.com'}
        with self.assertRaises(ValueError):remote_argv(config,Path('.'),None)

    def test_single_remote_request_keeps_operator_selection(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);(root/'request.json').write_text('{}')
            config={'endpoint':'http://127.0.0.1:18080','client_python':'candidate-python',
                    'project_id':'selected-project','client_wheel':'selected-wheel'}
            args=argparse.Namespace(operation='rehearse',request='request.json',key=None,destination=None)
            argv=remote_argv(config,root,args)
            self.assertEqual(argv[argv.index('--project')+1],'selected-project')
            self.assertEqual(argv[argv.index('--endpoint')+1],config['endpoint'])
            self.assertIn('--test-copy',argv)
            self.assertEqual(argv[argv.index('--request')+1],str(root/'request.json'))


if __name__=='__main__':unittest.main()
