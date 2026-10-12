"""Regression coverage for native discovery and exact failure/read displays."""
import contextlib
import io
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from native_call import main, result_fields
from qualify_agents import shell_prefix
from summarize_native import helper_reads, summarize


class NativeObservationTests(unittest.TestCase):
    def test_shell_prefix_preserves_the_existing_literal_grant(self):
        self.assertEqual('"C:/Program Files/python.exe" -I "C:/task/native_call.py"',
                         shell_prefix(['C:/Program Files/python.exe','-I','C:/task/native_call.py']))
        for argv in ([], ['python','-c','script'], ['python','-I','bad"path'],
                     ['$(command)','-I','script'], ['python','-I','bad`path'],
                     ['python','-I','bad\npath'], ['python','-I',None]):
            with self.subTest(argv=argv), self.assertRaises(ValueError):
                shell_prefix(argv)

    def test_failed_final_command_is_visible_before_large_successes(self):
        for exit_code in (0, 1):
            with self.subTest(exit_code=exit_code):
                result = {'outcome':'blocked' if exit_code else 'completed',
                          'blocked_by':['WEX-ECP-003: exact supplied diagnostic'] if exit_code else []}
                steps = [{'command':'check','exit':0,'result':{'detail':'x'*18000}} for _ in range(3)]
                steps.append({'command':'check','exit':exit_code,
                              'result':{'restitution':result,'history':'y'*20000}})
                raw = {'outcome':'refused' if exit_code else 'previewed',
                       'evaluator_output':{'commands':steps},'other':'z'*25000}
                view = result_fields(json.dumps(raw))
                self.assertEqual(raw['outcome'],view['fields']['/outcome'])
                self.assertEqual(exit_code,view['fields']['/evaluator_output/commands/3/exit'])
                self.assertEqual(result,view['fields']['/evaluator_output/commands/3/result/restitution'])
                self.assertIn('/evaluator_output/commands/3/result/history',view['omitted_pointers'])
                self.assertFalse(view['complete']);self.assertFalse(view['interpretation'])
                self.assertLessEqual(len(json.dumps(view).encode()),16*1024)
                # Every shown value is copied from the same original pointer.
                for pointer, value in view['fields'].items():
                    actual=raw
                    for key in pointer.strip('/').split('/'):
                        actual=actual[int(key)] if isinstance(actual,list) else actual[key]
                    self.assertEqual(actual,value)

    def test_malformed_command_shapes_stay_visible_without_interpretation(self):
        raw={'outcome':'refused','evaluator_output':{'commands':[None,'x'*4000,{'exit':1,'result':'z'*4000}]}}
        view=result_fields(json.dumps(raw))
        self.assertEqual(1,view['fields']['/evaluator_output/commands/2/exit'])
        self.assertIn('/evaluator_output/commands/2/result',view['omitted_pointers'])
        self.assertFalse(view['interpretation'])

    def test_helper_read_metadata_excludes_content_and_metadata_only_lookups(self):
        value={'resources':[{'path':'guide.md','sha256':'digest','sections':[
            {'heading':'Current step','content':'private source text','start_line':4,'end_line':8}]}]}
        result=helper_reads('python -I native_call.py instructions --section guide#step',json.dumps(value),5)
        self.assertEqual('guide.md',result[0]['path']);self.assertEqual(5,result[0]['line'])
        self.assertEqual([{'heading':'Current step','start_line':4,'end_line':8}],result[0]['sections'])
        self.assertNotIn('private source text',json.dumps(result))
        for command, output in [('native_call.py lookup-file guide.md',json.dumps(value)),
            ('cat guide.md',json.dumps(value)),('native_call.py read-text guide.md','{"truncated":'),
            ('native_call.py read-text guide.md',json.dumps({'path':'guide.md','sha256':'digest'}))]:
            self.assertEqual([],helper_reads(command,output,1))

    def test_summary_keeps_failed_attempts_separate_from_successful_reads(self):
        events=[
            {'message':{'content':[{'type':'thinking','thinking':'hidden-sentinel-123'},
                {'type':'tool_use','id':'failed','name':'Read','input':{'file_path':'missing.md'}},
                {'type':'tool_use','id':'read','name':'Read','input':{'file_path':'guide.md','limit':2}}]}},
            {'message':{'content':[{'type':'tool_result','tool_use_id':'failed','is_error':True,'content':'missing'},
                {'type':'tool_result','tool_use_id':'read','content':'two lines of source'}]}},
            {'type':'item.completed','item':{'id':'helper','type':'command_execution','exit_code':0,
                'command':'python -I native_call.py read-text chunk.md --offset 5',
                'aggregated_output':json.dumps({'path':'chunk.md','sha256':'hash','text':'actual text',
                    'offset':5,'next_offset':10,'complete':False})}},
            {'type':'item.completed','item':{'id':'denied','type':'command_execution','exit_code':1,
                'command':'python -I native_call.py read-text denied.md',
                'aggregated_output':json.dumps({'path':'denied.md','text':'not a success'})}}]
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);(root/'work').mkdir()
            (root/'session.json').write_text(json.dumps({'host':'codex','elapsed_seconds':10}))
            (root/'events.jsonl').write_text('\n'.join(json.dumps(x) for x in events)+'\n')
            value=summarize(root)
        self.assertEqual(['missing.md','guide.md'],[r['path'] for r in value['file_reads']])
        self.assertEqual(['guide.md','chunk.md'],[r['path'] for r in value['observed_content_reads']])
        self.assertIsNone(value['observed_content_reads'][0]['complete'])
        self.assertFalse(value['observed_content_reads'][1]['complete'])
        self.assertEqual(2,len(value['native_failures']));self.assertIsNone(value['native_calls'])
        self.assertNotIn('actual text',json.dumps(value));self.assertNotIn('hidden-sentinel-123',json.dumps(value))

    def test_observation_record_is_exact_new_work_file_with_compact_index(self):
        value={'snapshot':'in_progress','wall_seconds':None,'native_calls':None,'observed_tool_items':4,
            'native_call_count_complete':False,'peak_input_context':None,'limits':'observed only',
            'observed_content_reads':[{'path':'guide.md'}],'native_failures':[{'code':'FAILED'}],
            'failed_command_records':[],'command_records':[]}
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);selection=root/'selection.json';selection.write_text('{}')
            record=root/'work/observations.json'
            env={'HAG_NATIVE_WORK_DIRECTORY':str(root),'HAG_NATIVE_SELECTION':str(selection)}
            def invoke(path):
                out=io.StringIO()
                with patch.dict(os.environ,env),patch('sys.argv',['helper','observations','--record',str(path)]),\
                     patch('native_call.observations',return_value=value),contextlib.redirect_stdout(out):
                    self.assertEqual(0,main())
                return json.loads(out.getvalue())
            result=invoke(record)
            self.assertEqual(value,json.loads(record.read_text()))
            self.assertIn('/observed_content_reads',result['pointers'])
            self.assertNotIn('observed_content_reads',result)
            with self.assertRaises(ValueError):invoke(record)
            with self.assertRaises(ValueError):invoke(root/'inputs/new.json')
            with self.assertRaises(ValueError):invoke(root.parent/'outside.json')
            self.assertEqual(value,json.loads(record.read_text()))


if __name__ == '__main__':
    unittest.main()
