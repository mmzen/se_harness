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

from native_call import contained, remote_argv, main, read_json, lookup_file, find_file, result_fields
from qualify_agents import prepare_output
from assess_native import semantic_assertions


class NativeCallBoundaries(unittest.TestCase):
    def test_live_observations_preserve_failures_without_reasoning_or_final_claim(self):
        import hashlib
        from native_call import observations
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);inputs=root/'inputs';inputs.mkdir();(root/'work').mkdir()
            script=inputs/'summarize_native.py'
            script.write_bytes(Path(__file__).with_name('summarize_native.py').read_bytes())
            inventory=inputs/'inventory.json'
            inventory.write_text(json.dumps({'files':[{'relative':script.name,'path':str(script),'bytes':script.stat().st_size,'sha256':hashlib.sha256(script.read_bytes()).hexdigest()}]}))
            events=[{'message':{'content':[{'type':'thinking','thinking':'private content'},
                {'type':'tool_use','id':'failed','name':'Bash','input':{'description':'read selected sections'}}]}},
                {'message':{'content':[{'type':'tool_result','tool_use_id':'failed','is_error':True,'content':'missing heading'}]}}]
            (root/'events.jsonl').write_text('\n'.join(json.dumps(x) for x in events)+'\n{"partial":')
            result=observations(root,{'inputs_inventory':str(inventory)})
            self.assertEqual('in_progress',result['snapshot']);self.assertIsNone(result['wall_seconds'])
            self.assertEqual('unavailable',result['goals']['calls_at_most_15'])
            self.assertTrue(result['partial_event_line_omitted'])
            self.assertEqual('missing heading',result['native_failures'][0]['diagnostic'])
            self.assertNotIn('private content',json.dumps(result))
            self.assertEqual('not performed by this summary',result['content_review'])
            script.write_bytes(b'raise AssertionError("must not execute changed code")')
            with self.assertRaises(ValueError):observations(root,{'inputs_inventory':str(inventory)})

    def test_section_resource_ids_and_legacy_inventory_names_resolve_same_source(self):
        import hashlib
        from native_call import instructions
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);inputs=root/'inputs';inputs.mkdir()
            name='released-resources/docs/engineering/guide.md';source=inputs/name;source.parent.mkdir(parents=True)
            source.write_bytes(b'# Selected\nExact text.\n')
            inventory=inputs/'inventory.json';inventory.write_text(json.dumps({'files':[{'relative':name,'path':str(source),'bytes':source.stat().st_size,'sha256':hashlib.sha256(source.read_bytes()).hexdigest()}]}))
            config_file=root/'configuration.json';config_file.write_text(json.dumps({'components':{'evaluator':{'version':'0.22.1'}}}))
            config={'configuration':str(config_file),'evaluator_version':'0.22.1','inputs_inventory':str(inventory),'client_python':'installed-python'}
            with patch('native_call.subprocess.run',return_value=subprocess.CompletedProcess([],0,'{}','')) as run:
                instructions(root,config,['docs/engineering/guide.md#Selected'])
                first=run.call_args.kwargs['input']
                instructions(root,config,[name+'#Selected'])
                self.assertEqual(first,run.call_args.kwargs['input'])
                with self.assertRaises(ValueError):instructions(root,config,['../guide.md#Selected'])
                self.assertEqual(2,run.call_count)

    def test_typed_adapter_forwards_inputs_without_encoding_or_choosing_values(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);document=root/'draft.md';document.write_bytes(b'exact')
            args=argparse.Namespace(operation='revise-artifact',request=None,key=None,destination=None,
                typed=True,compact=True,include_document=False,record=str(root/'record.json'),
                document_file=str(document),operation_key='caller-key',expected_project_version='4',
                context='caller-context',context_version='2',artifact='INT-TST-001',expected_revision='caller-revision')
            config={'endpoint':'http://127.0.0.1:18080','client_python':'candidate-python','project_id':'selected-project','client_wheel':'candidate.whl'}
            with patch('native_call.subprocess.run') as run:
                argv=remote_argv(config,root,args)
                self.assertEqual(str(document),argv[argv.index('--document-file')+1])
                self.assertEqual('caller-key',argv[argv.index('--operation-key')+1])
                self.assertEqual(str(root/'record.json.evidence'),argv[argv.index('--record-directory')+1])
                self.assertNotIn('--request',argv)
            run.assert_not_called()

    def test_summary_retains_recovered_native_and_command_failures(self):
        from summarize_native import summarize
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);(root/'work').mkdir()
            (root/'session.json').write_text(json.dumps({'elapsed_seconds':200}))
            events=[{'message':{'id':'m1','usage':{'input_tokens':100,'cache_read_input_tokens':200},'content':[
                {'type':'tool_use','id':'c1','name':'Bash','input':{}}, {'type':'thinking','thinking':'private content'}]}},
                {'message':{'content':[{'type':'tool_result','tool_use_id':'c1','is_error':True,'content':'denied'}]}},
                {'message':{'id':'m2','usage':{'input_tokens':50,'cache_read_input_tokens':400},'content':[
                    {'type':'tool_use','id':'c2','name':'Bash','input':{}}]}}]
            (root/'events.jsonl').write_text('\n'.join(json.dumps(x) for x in events))
            for name,code in [('failed',2),('recovered',0)]:
                (root/'work'/f'{name}.json').write_text(json.dumps({'argv':['client'],'cwd':str(root),'exit':code,'stdout':'','stderr':''}))
            value=summarize(root)
            self.assertEqual(2,value['native_calls']);self.assertEqual(450,value['peak_input_context'])
            self.assertEqual(1,len(value['native_failures']));self.assertEqual(1,len(value['failed_command_records']))
            self.assertNotIn('private content',json.dumps(value))
            self.assertEqual('missed',value['goals']['wall_under_180'])

    def test_filename_search_is_bounded_ambiguous_and_never_selects(self):
        import hashlib
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);inputs=root/'inputs';inputs.mkdir();entries=[]
            for number in range(22):
                path=inputs/str(number)/'guide.md';path.parent.mkdir();path.write_bytes(b'exact')
                entries.append({'relative':path.relative_to(inputs).as_posix(),'path':str(path),'bytes':5,'sha256':hashlib.sha256(b'exact').hexdigest()})
            inventory=inputs/'inventory.json';inventory.write_text(json.dumps({'files':entries}));config={'inputs_inventory':str(inventory)}
            with patch('native_call.subprocess.run') as run:
                result=find_file(root,config,'guide.md')
                self.assertEqual(result['total_matches'],22);self.assertEqual(len(result['matches']),20)
                self.assertFalse(result['complete']);self.assertIsNone(result['selection'])
                narrowed=find_file(root,config,'guide.md','2/')
                self.assertTrue(narrowed['complete']);self.assertEqual(narrowed['matches'],[entries[2]])
                self.assertEqual(find_file(root,config,'absent.md')['matches'],[])
                for name in ('','../guide.md','*','dir\\guide.md','..'):
                    with self.assertRaises(ValueError):find_file(root,config,name)
                with self.assertRaises(ValueError):find_file(root,config,'guide.md','../')
                Path(entries[2]['path']).write_bytes(b'changed')
                with self.assertRaisesRegex(ValueError,'no longer'):find_file(root,config,'guide.md','2/')
            run.assert_not_called()

    def test_base64_reader_preserves_utf8_bytes_and_rejects_invalid_or_secret_text(self):
        import base64,hashlib
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);p=root/'revision.json';raw='+++\r\nid = "INT-T-001"\r\n+++\nCafé\n'.encode()
            p.write_text(json.dumps({'data':{'document_base64':base64.b64encode(raw).decode()}}))
            with patch('native_call.subprocess.run') as run:
                value=read_json(root,p,'/data/document_base64',decode_base64=True)
                self.assertEqual(value['value'].encode(),raw)
                self.assertEqual(value['decoded_sha256'],hashlib.sha256(raw).hexdigest())
                with self.assertRaises(ValueError):read_json(root,p,'/data',decode_base64=True)
                with self.assertRaises(ValueError):read_json(root,p,'/data/document_base64',keys=True,decode_base64=True)
                for encoded in ('not base64','Zh==','/w=='):
                    p.write_text(json.dumps(encoded))
                    with self.assertRaises(ValueError):read_json(root,p,'',decode_base64=True)
                with patch.dict(os.environ,{'HAG_NATIVE_TEST_TOKEN':'private-test-token'}):
                    p.write_text(json.dumps(base64.b64encode(b'private-test-token').decode()))
                    with self.assertRaisesRegex(ValueError,'credential'):read_json(root,p,'',decode_base64=True)
            run.assert_not_called()

    def test_lookup_verifies_one_exact_file_and_rejects_changed_or_ambiguous_inputs(self):
        import hashlib
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory); inputs=root/'inputs'; inputs.mkdir()
            path=inputs/'guide.md';path.write_bytes(b'original')
            entry={'relative':'guide.md','path':str(path),'bytes':8,'sha256':hashlib.sha256(b'original').hexdigest()}
            inventory=inputs/'inventory.json';config={'inputs_inventory':str(inventory)}
            inventory.write_text(json.dumps({'files':[entry]}))
            with patch('native_call.subprocess.run') as run:
                self.assertEqual(lookup_file(root,config,'guide.md')['file'],entry)
                self.assertFalse(lookup_file(root,config,'guide.md')['content_read'])
            run.assert_not_called()
            with self.assertRaises(ValueError):lookup_file(root,config,'../guide.md')
            path.write_bytes(b'modified')
            with self.assertRaisesRegex(ValueError,'no longer'):lookup_file(root,config,'guide.md')
            inventory.write_text(json.dumps({'files':[entry,entry]}))
            with self.assertRaisesRegex(ValueError,'one exact'):lookup_file(root,config,'guide.md')
            entry['path']=str(root/'guide.md')
            inventory.write_text(json.dumps({'files':[entry]}))
            with self.assertRaisesRegex(ValueError,'relative name'):lookup_file(root,config,'guide.md')

    def test_small_result_view_keeps_refusals_and_explicitly_marks_omissions(self):
        raw=json.dumps({'outcome':'refused','evaluator_output':{'errors':[{'id':'FAILED','passed':False}],
            'complete':False,'history':'x'*80000},'a/b':{'~':None}})
        view=result_fields(raw)
        self.assertEqual(view['fields']['/outcome'],'refused')
        self.assertEqual(view['fields']['/evaluator_output/errors'],[{'id':'FAILED','passed':False}])
        self.assertIs(view['fields']['/evaluator_output/complete'],False)
        self.assertIn('/evaluator_output/history',view['omitted_pointers'])
        self.assertFalse(view['complete']);self.assertFalse(view['interpretation'])
        self.assertLessEqual(len(json.dumps(view).encode()),16*1024)
        self.assertFalse(result_fields('not json')['json'])
        self.assertEqual(result_fields('{"accepted":false}')['fields'][''],{'accepted':False})
        many=result_fields(json.dumps({'x'*100+str(i):'y'*9000 for i in range(1000)}))
        self.assertEqual(many['omitted_pointers'],[''])

    def test_json_read_preserves_exact_values_and_pointers_without_execution(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory); path=root/'receipt.json'
            raw=b'{"outcome":"refused","a/b":{"~x":[null,false,"not accepted"]}}\n'
            path.write_bytes(raw)
            with patch('native_call.subprocess.run') as run:
                selected=read_json(root,path,'/a~1b/~0x/2')
                self.assertEqual(selected['value'],'not accepted')
                self.assertEqual(selected['pointer'],'/a~1b/~0x/2')
                self.assertTrue(selected['selection_only'])
                self.assertEqual(read_json(root,path,'/a~1b/~0x/0')['value'],None)
                self.assertIs(read_json(root,path,'/a~1b/~0x/1')['value'],False)
                self.assertEqual(read_json(root,path,'',True)['keys'],['outcome','a/b'])
                self.assertEqual(read_json(root,path,'/a~1b/~0x',True)['length'],3)
                self.assertEqual(read_json(root,path,json.dumps('/a~1b/~0x/2')),selected)
                self.assertEqual(read_json(root,path,'""',True)['keys'],['outcome','a/b'])
            run.assert_not_called();self.assertEqual(path.read_bytes(),raw)

    def test_json_read_refuses_escape_missing_fields_credentials_and_oversize(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);path=root/'receipt.json'
            path.write_text(json.dumps({'large':'x'*70000,'values':[1]}))
            for pointer in ('/missing','/values/01','/values/-1','/values/1','/values/0/x','bad','/~2','"bad"','"unfinished'):
                with self.assertRaises(ValueError):read_json(root,path,pointer)
            with self.assertRaises(ValueError):read_json(root,'../receipt.json','')
            with self.assertRaisesRegex(ValueError,'64 KiB'):read_json(root,path,'/large')
            self.assertEqual(read_json(root,path,'',True)['keys'],['large','values'])
            with patch.dict(os.environ,{'HAG_NATIVE_TEST_TOKEN':'private-test-token'}):
                path.write_text('{"secret":"private-test-token"}')
                with self.assertRaisesRegex(ValueError,'credential'):read_json(root,path,'',True)
            path.write_bytes(b' '*(4*1024*1024+1))
            with self.assertRaisesRegex(ValueError,'4 MiB'):read_json(root,path,'')

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
