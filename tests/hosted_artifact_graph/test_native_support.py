"""Boundaries of the one-call native qualification helper."""
import argparse
import contextlib
import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
from pathlib import Path

from native_call import contained, remote_argv, main
from qualify_agents import prepare_output
from assess_native import semantic_assertions


class NativeCallBoundaries(unittest.TestCase):
    def test_readable_output_preserves_complete_result_and_exit(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory); selection=root/'selection.json'
            selection.write_text(json.dumps({'endpoint':'http://127.0.0.1:18080',
                'client_python':'candidate-python','project_id':'selected-project'}))
            stdout='{"outcome":"refused","detail":"line one\\nline two"}\n'
            outcome=subprocess.CompletedProcess([],1,stdout,'actual diagnostic')
            record=root/'result.json'; capture=io.StringIO()
            with patch.dict(os.environ,{'HAG_NATIVE_WORK_DIRECTORY':str(root),
                    'HAG_NATIVE_SELECTION':str(selection),'HAG_NATIVE_TEST_TOKEN':'private-test-token'}), \
                 patch.object(sys,'argv',['helper','remote','status','--record',str(record)]), \
                 patch('native_call.subprocess.run',return_value=outcome) as run, \
                 contextlib.redirect_stdout(capture):
                self.assertEqual(main(),1)
            run.assert_called_once()
            original=json.loads(record.read_text())
            self.assertEqual(original['stdout'],stdout)
            self.assertEqual(original['stderr'],'actual diagnostic')
            display=json.loads(capture.getvalue())
            self.assertEqual(Path(display['stdout_file']).read_bytes(),stdout.encode())
            self.assertEqual(display['exit'],1)
            # A pre-existing companion refuses before any command can run.
            record.unlink()
            with patch.dict(os.environ,{'HAG_NATIVE_WORK_DIRECTORY':str(root),
                    'HAG_NATIVE_SELECTION':str(selection)}), \
                 patch.object(sys,'argv',['helper','remote','status','--record',str(record)]), \
                 patch('native_call.subprocess.run') as run:
                with self.assertRaises(ValueError):main()
            run.assert_not_called()

    def test_receipt_key_order_is_incidental_but_state_is_not(self):
        value={'state':{'after':[{'id':'WO-T-001','status':'approved'}]},
            'restitution':{'current_lifecycle_state':['WO-T-001 is approved.'],
                          'next':{'procedure_id':'PROC-WO-START','step_id':'STEP-WO-START-PREFLIGHT'}}}
        stored=json.loads(json.dumps(value,sort_keys=True))
        self.assertEqual(semantic_assertions(value),semantic_assertions(stored))
        stored['state']['after'][0]['status']='draft'
        self.assertNotEqual(semantic_assertions(value),semantic_assertions(stored))

    def test_prepared_run_cannot_overwrite_prior_results(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            (root/'inputs').mkdir(); (root/'work').mkdir()
            prepare_output(root,True)
            (root/'events.jsonl').write_text('prior evidence')
            with self.assertRaises(ValueError): prepare_output(root,True)
            self.assertEqual((root/'events.jsonl').read_text(),'prior evidence')

    def test_prepared_run_requires_empty_work(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            (root/'inputs').mkdir(); (root/'work').mkdir()
            (root/'work/request.json').write_text('{}')
            with self.assertRaises(ValueError): prepare_output(root,True)

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
