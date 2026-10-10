"""Boundaries of the one-call native qualification helper."""
import argparse
import contextlib
import hashlib
import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
from pathlib import Path

from native_call import contained, remote_argv, main, read_json, lookup_file, find_file, result_fields, read_text_files
from qualify_agents import prepare_output, instruction_entry, write_prompt, prompt_pointer, codex_loopback_options, run as run_native
from assess_native import semantic_assertions


class NativeCallBoundaries(unittest.TestCase):
    def test_loopback_profile_refuses_other_hosts_and_ambiguous_destinations(self):
        for host, endpoint in [('claude','http://127.0.0.1:8000'),
                ('codex','https://example.com:443'),('codex','http://localhost:8000'),
                ('codex','http://127.0.0.1'),('codex','http://user@127.0.0.1:8000'),
                ('codex','http://127.0.0.1:8000/path'),('codex','http://127.0.0.1:8000?x')]:
            with self.subTest(host=host,endpoint=endpoint), self.assertRaises(ValueError):
                codex_loopback_options(host,endpoint)
        import tomllib
        args=codex_loopback_options('codex','http://127.0.0.1:8000')
        config=tomllib.loads('\n'.join(args[1::2]))
        profile=config['permissions'][config['default_permissions']]
        self.assertEqual(':workspace',profile['extends'])
        self.assertTrue(config['features']['network_proxy'])
        self.assertEqual({'127.0.0.1':'allow'},profile['network']['domains'])
        self.assertEqual('auto_review',config['approvals_reviewer'])

    def test_batch_text_preserves_exact_selected_bytes_and_refuses_unsafe_inputs(self):
        import hashlib
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory); inputs=root/'inputs'; inputs.mkdir(); (root/'work').mkdir()
            first=inputs/'one.md'; first.write_bytes('One\r\n“Exact”.\n'.encode())
            second=root/'work/two.md'; second.write_bytes(b'Two\n')
            inventory=inputs/'inventory.json'
            inventory.write_text(json.dumps({'files':[{'path':str(first),'relative':'one.md',
                'bytes':first.stat().st_size,'sha256':hashlib.sha256(first.read_bytes()).hexdigest()}]}))
            config={'inputs_inventory':str(inventory)}
            values=read_text_files(root,config,[first,second])['files']
            self.assertEqual([first.read_bytes(),second.read_bytes()],[x['text'].encode() for x in values])
            self.assertEqual(values[0],read_text_files(root,config,[first]))
            for paths in ([],[first]*9,[first,root/'../outside'],[first,root/'selection.json']):
                with self.subTest(paths=paths),self.assertRaises((ValueError,OSError)):
                    read_text_files(root,config,paths)
            first.write_bytes(b'changed staged input')
            with self.assertRaisesRegex(ValueError,'inventory'):
                read_text_files(root,config,[first,second])
            with patch.dict(os.environ,{'HAG_NATIVE_TEST_TOKEN':'synthetic-secret'}):
                second.write_bytes(b'synthetic-secret')
                with self.assertRaisesRegex(ValueError,'credential'):
                    read_text_files(root,config,[second])
            second.write_text('x'*40000)
            with self.assertRaisesRegex(ValueError,'64 KiB'):
                read_text_files(root,config,[second,second])

    def test_startup_pointer_leaves_task_bytes_in_one_readable_location(self):
        with tempfile.TemporaryDirectory() as directory:
            task = Path(directory)/'task with spaces.md'
            raw = '## Canonical\r\nExact “instruction”.\nRequested outcome.\n'.encode()
            task.write_bytes(raw)
            prompt = prompt_pointer(task)
            self.assertIn(str(task), prompt)
            self.assertNotIn(raw.decode(), prompt)
            self.assertEqual(raw, task.read_bytes())
            self.assertIn('before your first explanation', prompt)
            self.assertIn('After compaction', prompt)

    def test_pinned_task_recovery_preserves_chunks_and_refuses_other_root_content(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory); task=root/'task.md'
            raw=('Exact \U0001f600\r\n' * 1000).encode(); task.write_bytes(raw)
            digest=hashlib.sha256(raw).hexdigest()
            with patch.dict(os.environ,{'HAG_NATIVE_ENTRY_SHA256':digest}):
                offset=0; recovered=''
                while True:
                    result=read_text_files(root,{},[task],offset=offset,limit=4096)
                    recovered+=result['text']
                    self.assertEqual(digest,result['sha256'])
                    self.assertEqual(len(raw),result['bytes'])
                    self.assertLessEqual(len(json.dumps(result).encode()),65536)
                    if result['complete']: break
                    self.assertGreater(result['next_offset'],offset)
                    offset=result['next_offset']
                self.assertEqual(raw,recovered.encode())
                for name in ('events.jsonl','invocation.json','credentials.json'):
                    path=root/name; path.write_bytes(raw)
                    with self.assertRaisesRegex(ValueError,'restricted'):
                        read_text_files(root,{},[path],offset=0)
                is_link=Path.is_symlink
                with patch.object(Path,'is_symlink',lambda path:path==task or is_link(path)):
                    with self.assertRaisesRegex(ValueError,'Linked'):
                        read_text_files(root,{},[task],offset=0)
                for paths,offset,limit in [([task,task],0,1),([task],-1,1),
                        ([task],len(recovered)+1,1),([task],0,0),([task],0,4097)]:
                    with self.assertRaises(ValueError):
                        read_text_files(root,{},paths,offset,limit)
                task.write_bytes(raw+b'changed')
                with self.assertRaisesRegex(ValueError,'pinned identity'):
                    read_text_files(root,{},[task],offset=0)
            with patch.dict(os.environ,{'HAG_NATIVE_ENTRY_SHA256':''}):
                with self.assertRaisesRegex(ValueError,'pinned identity'):
                    read_text_files(root,{},[task],offset=0)

    def test_complete_entry_reaches_host_stdin_once_and_task_recovery_is_pinned(self):
        for host_name in ('claude','codex'):
            for complete in (False,True):
                with self.subTest(host=host_name,complete=complete),tempfile.TemporaryDirectory() as directory:
                    root=Path(directory);output=root/'native'
                    selection=root/'selected.json'
                    selection.write_text(json.dumps({'endpoint':'http://127.0.0.1:8000','plugin':str(root/'plugin')}))
                    credentials=root/'credentials.json'
                    credentials.write_text(json.dumps({'principals':[{'id':'operator','token':'synthetic-test-secret'}]}))
                    task=root/'request.md';task.write_text('Unique requested outcome.\n')
                    args=argparse.Namespace(output=output,prepared_inputs=False,selection=selection,
                        credentials=credentials,host=host_name,drop_reply=False,complete_inputs=complete,
                        instruction_section=['guide.md#canonical'],task=task,executable='native-host',
                        model=None,permission_settings=None,timeout=10)
                    with (patch('qualify_agents.instruction_entry',return_value=({'sections':[]},'## Exact\r\nRule.\n')),
                         patch('qualify_agents.subprocess.Popen') as process,
                         patch('qualify_agents.write_prompt') as writer,contextlib.redirect_stdout(io.StringIO())):
                        child=process.return_value.__enter__.return_value
                        child.stdout=[];child.wait.return_value=0
                        self.assertEqual(0,run_native(args))
                    raw=(output/'task.md').read_bytes()
                    sent=writer.call_args.args[1]
                    self.assertEqual(raw.decode() if complete else prompt_pointer(output/'task.md'),sent)
                    self.assertEqual(hashlib.sha256(raw).hexdigest(),process.call_args.kwargs['env']['HAG_NATIVE_ENTRY_SHA256'])
                    if host_name=='claude':
                        locator=(output/'CLAUDE.md').read_text()
                        self.assertNotIn('Unique requested outcome.',locator)
                        if complete:self.assertNotIn('selection.json',locator)
                    invocation=json.loads((output/'invocation.json').read_bytes())
                    self.assertEqual('stdin-complete-entry' if complete else 'stdin-file-pointer',invocation['prompt_transport'])
                    self.assertEqual(hashlib.sha256(sent.encode()).hexdigest(),invocation['input_sha256']['effective_prompt'])

    def test_native_stdin_preserves_utf8_and_mixed_canonical_line_endings(self):
        raw = '## Exact\nUnicode “text”.\r\nNext.\n'.encode()
        with subprocess.Popen([sys.executable, '-I', '-c',
                'import sys;sys.stdout.buffer.write(sys.stdin.buffer.read())'],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                text=True, encoding='utf-8') as child:
            child.stdin.reconfigure(newline='\r\n')
            write_prompt(child.stdin, raw.decode())
            self.assertEqual(raw, child.stdout.buffer.read())
            self.assertEqual(0, child.wait(timeout=10))

    def test_opening_entry_keeps_canonical_bytes_and_only_pointers_to_artifacts(self):
        import hashlib
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); inputs = root/'inputs'; inputs.mkdir()
            artifact = inputs/'source/REQ-TST-001.md'; artifact.parent.mkdir()
            raw = b'private fixture content, not an opening answer\n'
            artifact.write_bytes(raw)
            manifest = inputs/'source-manifest.json'
            item = {'artifact_id':'REQ-TST-001', 'path':'REQ-TST-001.md',
                    'bytes':len(raw), 'raw_sha256':hashlib.sha256(raw).hexdigest()}
            manifest.write_text(json.dumps({'artifacts':[item]}))
            inventory = inputs/'inventory.json'
            inventory.write_text(json.dumps({'files':[
                {'relative':p.relative_to(inputs).as_posix(), 'path':str(p),
                 'bytes':p.stat().st_size, 'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
                for p in (manifest, artifact)]}))
            settings = {'source_manifest':str(manifest), 'inputs_inventory':str(inventory)}
            content = '## Exact section\r\nKeep “these” bytes.\r\n'
            view = {'resources':[{'resource':'guide.md','path':'selected-release/guide.md',
                'release':{'version':'0.22.1'},'sha256':'source-sha',
                'sections':[{'content':content}]}]}
            with patch('qualify_agents.instructions', return_value=view) as reader:
                packet, text = instruction_entry(root, settings, ['guide.md#exact-section'])
                reader.assert_called_once_with(root, settings, ['guide.md#exact-section'])
                self.assertIn(content, text)
                self.assertNotIn(raw.decode(), text)
                self.assertEqual(str(artifact), packet['artifact_pointers'][0]['path'])
                self.assertEqual(view, packet['instruction_view'])
                artifact.write_bytes(b'changed')
                with self.assertRaises(ValueError):
                    instruction_entry(root, settings, ['guide.md#exact-section'])
                artifact.write_bytes(raw)
                item['raw_sha256'] = 'wrong'
                manifest.write_text(json.dumps({'artifacts':[item]}))
                entries = json.loads(inventory.read_text())
                entries['files'][0].update(bytes=manifest.stat().st_size,
                    sha256=hashlib.sha256(manifest.read_bytes()).hexdigest())
                inventory.write_text(json.dumps(entries))
                with self.assertRaisesRegex(ValueError, 'Source-manifest identity'):
                    instruction_entry(root, settings, ['guide.md#exact-section'])
                settings['source_manifest'] = str(root/'../outside.json')
                with self.assertRaises(ValueError):
                    instruction_entry(root, settings, ['guide.md#exact-section'])

    def test_opening_entry_preserves_instruction_discovery_refusal(self):
        with patch('qualify_agents.instructions', side_effect=ValueError('ambiguous heading')):
            with self.assertRaisesRegex(ValueError, 'ambiguous heading'):
                instruction_entry(Path('.'), {}, ['guide.md#duplicate'])

    def complete_entry_fixture(self, root):
        inputs=root/'inputs'; inputs.mkdir()
        paths={
            'source/REQ-TST-001.md':b'Original requirement\r\n```markdown\nNot an answer.\n```\n',
            'source/unrelated.txt':'Every source is included, even “unrelated”.\n'.encode(),
            'native-tools.md':b'Original tool capabilities\n',
            'combination.json':b'{"component":"original"}\n',
            'plugin/skills/setup/references/hosted-context.md':b'Exact setup reference\r\n',
            'plugin/skills/change/references/hosted-drafts.md':b'Exact drafting reference\n',
        }
        for name,raw in paths.items():
            path=inputs/name;path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(raw)
        raw=paths['source/REQ-TST-001.md']
        manifest=inputs/'source-manifest.json'
        manifest.write_text(json.dumps({'artifacts':[{'artifact_id':'REQ-TST-001',
            'path':'REQ-TST-001.md','bytes':len(raw),'raw_sha256':hashlib.sha256(raw).hexdigest()}]}))
        inventory=inputs/'inventory.json'
        self.refresh_entry_inventory(inputs,inventory)
        settings={'source_manifest':str(manifest),'inputs_inventory':str(inventory),
            'source_directory':str(inputs/'source'),'tool_index':str(inputs/'native-tools.md'),
            'combination':str(inputs/'combination.json'),'plugin':str(inputs/'plugin')}
        (root/'selection.json').write_text(json.dumps(settings))
        view={'resources':[{'resource':'guide.md','path':'released/guide.md',
            'release':{'version':'0.22.1'},'sha256':'canonical-identity',
            'sections':[{'content':'## Canonical\r\nAn exact rule.\n'}]}]}
        return settings,view,paths

    def refresh_entry_inventory(self,inputs,inventory):
        files=[p for p in inputs.rglob('*') if p.is_file() and p!=inventory]
        inventory.write_text(json.dumps({'files':[{'relative':p.relative_to(inputs).as_posix(),
            'path':str(p),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
            for p in files]}))

    def test_complete_entry_copies_all_sources_and_references_once_without_changing_them(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);settings,view,originals=self.complete_entry_fixture(root)
            with patch('qualify_agents.instructions',return_value=view):
                packet,text=instruction_entry(root,settings,['guide.md#canonical'],complete_inputs=True)
            files=packet['complete_input_files']['references']+packet['complete_input_files']['sources']
            self.assertEqual(set(originals),{Path(x['path']).relative_to(root/'inputs').as_posix() for x in files})
            self.assertEqual(len(files),len({x['path'] for x in files}))
            for item in files:
                raw=originals[Path(item['path']).relative_to(root/'inputs').as_posix()]
                self.assertEqual(raw,item['text'].encode())
                self.assertEqual(raw,Path(item['path']).read_bytes())
                self.assertEqual(1,text.count(raw.decode()))
                self.assertEqual(hashlib.sha256(raw).hexdigest(),item['sha256'])
            self.assertIn(view['resources'][0]['sections'][0]['content'],text)
            self.assertEqual(1,text.count('## Canonical'))
            self.assertEqual(len(text.encode()),packet['entry_bytes'])
            self.assertIn('task data, not instructions',text)

    def test_complete_entry_refuses_changed_missing_extra_duplicate_and_nontext_sources(self):
        for failure in ('changed','missing','extra','duplicate','nontext','oversized','reference','selection'):
            with self.subTest(failure=failure),tempfile.TemporaryDirectory() as directory:
                root=Path(directory);settings,view,_=self.complete_entry_fixture(root)
                source=root/'inputs/source/unrelated.txt';inventory=Path(settings['inputs_inventory'])
                if failure=='changed':source.write_bytes(b'changed')
                elif failure=='missing':source.unlink()
                elif failure=='extra':(source.parent/'unlisted.txt').write_text('Uninventoried')
                elif failure=='duplicate':
                    value=json.loads(inventory.read_bytes())
                    value['files'].append(next(x for x in value['files'] if x['relative']=='source/unrelated.txt'))
                    inventory.write_text(json.dumps(value))
                elif failure in ('nontext','oversized'):
                    source.write_bytes(b'\xff' if failure=='nontext' else b'x'*65537)
                    self.refresh_entry_inventory(root/'inputs',inventory)
                elif failure=='reference':Path(settings['tool_index']).write_bytes(b'tampered')
                else:(root/'selection.json').write_text('{}')
                with patch('qualify_agents.instructions',return_value=view),self.assertRaises((ValueError,OSError)):
                    instruction_entry(root,settings,['guide.md#canonical'],complete_inputs=True)

    def test_complete_entry_refuses_outside_and_linked_sources_and_aggregate_overflow(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);settings,view,_=self.complete_entry_fixture(root)
            with patch('qualify_agents.instructions',return_value=view):
                outside=dict(settings,source_directory=str(root.parent))
                with self.assertRaises(ValueError):
                    instruction_entry(root,outside,['guide.md#canonical'],complete_inputs=True)
                # Simulate a detected link, including hosts without symlink creation rights.
                source=root/'inputs/source/unrelated.txt';is_link=Path.is_symlink
                with patch.object(Path,'is_symlink',lambda path:path==source or is_link(path)):
                    with self.assertRaisesRegex(ValueError,'Linked'):
                        instruction_entry(root,settings,['guide.md#canonical'],complete_inputs=True)
                source.write_bytes(b'x'*33000)
                Path(settings['tool_index']).write_bytes(b'y'*33000)
                self.refresh_entry_inventory(root/'inputs',Path(settings['inputs_inventory']))
                with self.assertRaisesRegex(ValueError,'64 KiB'):
                    instruction_entry(root,settings,['guide.md#canonical'],complete_inputs=True)

    def test_complete_task_refuses_overflow_or_credential_before_host_start_or_capture(self):
        for content,diagnostic in [('x'*65536,'64 KiB'),('synthetic-test-secret','credential')]:
            with self.subTest(diagnostic=diagnostic),tempfile.TemporaryDirectory() as directory:
                root=Path(directory);output=root/'native'
                selection=root/'selected.json';selection.write_text('{"endpoint":"http://127.0.0.1:8000"}')
                credentials=root/'credentials.json'
                credentials.write_text(json.dumps({'principals':[{'id':'operator','token':'synthetic-test-secret'}]}))
                task=root/'request.md';task.write_text(content)
                args=argparse.Namespace(output=output,prepared_inputs=False,selection=selection,
                    credentials=credentials,host='claude',drop_reply=False,complete_inputs=True,
                    instruction_section=['guide.md#canonical'],task=task)
                with patch('qualify_agents.instruction_entry',return_value=({'sections':[]},'## Entry\n')),\
                     patch('qualify_agents.subprocess.Popen') as host,\
                     self.assertRaisesRegex(ValueError,diagnostic):
                    run_native(args)
                host.assert_not_called()
                self.assertFalse((output/'instruction-entry.json').exists())
                self.assertFalse((output/'task.md').exists())

    def test_text_read_is_exact_bounded_and_cannot_read_host_capture(self):
        import hashlib
        from native_call import read_text
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);inputs=root/'inputs';inputs.mkdir();work=root/'work';work.mkdir()
            source=inputs/'skill.md';raw='Exact “UTF-8” text.\r\n'.encode();source.write_bytes(raw)
            inventory=inputs/'inventory.json';inventory.write_text(json.dumps({'files':[{'relative':'skill.md','path':str(source),'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}]}))
            config={'inputs_inventory':str(inventory)}
            result=read_text(root,config,source)
            self.assertEqual(raw,result['text'].encode());self.assertEqual(hashlib.sha256(raw).hexdigest(),result['sha256'])
            (root/'events.jsonl').write_text('private capture')
            with self.assertRaises(ValueError):read_text(root,config,work/'../events.jsonl')
            with self.assertRaises(ValueError):read_text(root,config,root/'events.jsonl')
            source.write_bytes(b'changed')
            with self.assertRaises(ValueError):read_text(root,config,source)
            document=work/'draft.md';document.write_bytes(b'x'*65537)
            with self.assertRaises(ValueError):read_text(root,config,document)
            document.write_bytes(b'private-test-token')
            with patch.dict(os.environ,{'HAG_NATIVE_TEST_TOKEN':'private-test-token'}):
                with self.assertRaises(ValueError):read_text(root,config,document)

    def test_codex_capture_is_not_a_complete_native_call_count(self):
        from summarize_native import summarize
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);(root/'work').mkdir()
            (root/'session.json').write_text(json.dumps({'host':'codex','elapsed_seconds':80}))
            (root/'events.jsonl').write_text('Reading additional input from stdin...\n'+json.dumps({'type':'item.completed','item':{'type':'file_change','id':'c1','status':'completed'}})+'\n')
            result=summarize(root)
            self.assertIsNone(result['native_calls']);self.assertIsNone(result['peak_input_context'])
            self.assertEqual(1,result['observed_tool_items']);self.assertEqual([1],result['non_json_diagnostic_lines'])
            self.assertEqual('unavailable',result['goals']['calls_at_most_15'])

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
