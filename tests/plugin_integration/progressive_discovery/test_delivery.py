"""Protocol fixtures are not proof that a native host invoked an event."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ROOT/'plugins/verity-plane/common/scripts/inject_instructions.py'
spec = importlib.util.spec_from_file_location('instruction_delivery', SCRIPT)
delivery = importlib.util.module_from_spec(spec)
spec.loader.exec_module(delivery)


class InstructionDeliveryTests(unittest.TestCase):
    def setUp(self):
        temporary=tempfile.TemporaryDirectory(prefix='instruction-delivery-')
        self.addCleanup(temporary.cleanup)
        self.base=Path(temporary.name).resolve()
        self.data=self.base/'private'
        environment=patch.dict(os.environ, {'PLUGIN_DATA':str(self.data),'CLAUDE_PLUGIN_DATA':str(self.data)})
        environment.start()
        self.addCleanup(environment.stop)
        self.repo=self.fixture('first','0.19.0','A complete root.\n')

    def fixture(self,name,version,body,newline='\n'):
        repo=self.base/name
        repo.mkdir()
        text=f'# Engineering Harness for {name}\n\nThis repository uses SE Harness {version}.\n\n{body}'
        (repo/'ENGINEERING_HARNESS.md').write_bytes(text.replace('\n',newline).encode('utf-8'))
        (repo/'.engineering-harness.toml').write_text(f'[harness]\ntool_version = "{version}"\n',encoding='utf-8')
        lock={'schema':3,'tool_version':version,'hash_algorithm':'sha256','hash_mode':'utf8-text-lf-v1',
              'evaluator':{'version':version},'files':{'ENGINEERING_HARNESS.md':{'mode':'managed','sha256':hashlib.sha256(text.encode('utf-8')).hexdigest()}}}
        (repo/'.engineering-harness.lock').write_text(json.dumps(lock),encoding='utf-8')
        return repo

    def event(self,source='startup',repo=None):
        return {'hook_event_name':'SessionStart','source':source,'cwd':str(repo or self.repo),'session_id':'fixture-session'}

    def context(self,event=None,host='codex'):
        return delivery.respond(event or self.event(),host)['hookSpecificOutput']['additionalContext']

    def test_each_supported_event_returns_the_complete_current_root(self):
        for host,sources in delivery.SOURCES.items():
            for source in sources:
                with self.subTest(host=host,source=source):
                    context=self.context(self.event(source),host)
                    self.assertTrue(context.endswith((self.repo/'ENGINEERING_HARNESS.md').read_text(encoding='utf-8')))
                    self.assertIn('Selected release: 0.19.0',context)
                    self.assertIn(str(self.repo/'ENGINEERING_HARNESS.md'),context)

    def test_repository_switch_and_compaction_do_not_reuse_cached_policy(self):
        second=self.fixture('second','0.18.0','A different selected release.\n',newline='\r\n')
        first=self.context()
        current=self.context(self.event('compact',second),'claude')
        self.assertIn('A complete root.',first)
        self.assertIn('Selected release: 0.18.0',current)
        self.assertNotIn('A complete root.',current)
        self.assertIn('A different selected release.',current)

    def test_tampered_missing_and_mismatched_inputs_report_delivery_gap(self):
        files=['ENGINEERING_HARNESS.md','.engineering-harness.lock','.engineering-harness.toml']
        original={name:(self.repo/name).read_bytes() for name in files}
        for name in files:
            with self.subTest(name=name):
                (self.repo/name).unlink()
                self.assertIn('delivery is unavailable',self.context())
                (self.repo/name).write_bytes(original[name])
        (self.repo/'ENGINEERING_HARNESS.md').write_bytes(original['ENGINEERING_HARNESS.md']+b'tampered')
        self.assertIn('does not match',self.context())
        (self.repo/'ENGINEERING_HARNESS.md').write_bytes(original['ENGINEERING_HARNESS.md'])
        (self.repo/'.engineering-harness.toml').write_bytes(original['.engineering-harness.toml'].replace(b'0.19.0',b'0.18.0'))
        self.assertIn('do not select the same',self.context())

    def test_nested_damaged_selection_and_git_boundary_never_borrow_parent(self):
        child=self.repo/'child'
        child.mkdir()
        (child/'.engineering-harness.toml').write_text('[harness]\n',encoding='utf-8')
        self.assertIn('delivery is unavailable',self.context(self.event(repo=child)))
        (child/'.engineering-harness.toml').unlink()
        (child/'.git').mkdir()
        self.assertIn('# Select the working repository',self.context(self.event(repo=child)))
        (child/'.git').rmdir()
        self.assertIn('A complete root.',self.context(self.event(repo=child)))

    def test_limits_refuse_instead_of_truncating_policy(self):
        large=self.fixture('large','0.19.0','x'*10001)
        self.assertIn('no truncated policy',self.context(self.event(repo=large)))
        self.assertNotIn('x'*100,self.context(self.event(repo=large)))
        wide=self.fixture('wide','0.19.0','\U0001f642'*5001)
        self.assertIn('no truncated policy',self.context(self.event(repo=wide)))

    def test_concurrent_selection_change_refuses_mixed_inputs(self):
        original=delivery.read_regular
        count=0
        def changing(path,limit):
            nonlocal count
            raw=original(path,limit)
            if path.name=='.engineering-harness.toml':
                count+=1
                if count==2:return raw+b'\n'
            return raw
        with patch.object(delivery,'read_regular',side_effect=changing):
            self.assertIn('changed during delivery',self.context())

    def test_full_real_root_envelope_includes_long_path_and_unicode_units(self):
        # Use the real shipped root, not a short stand-in. The repository path
        # contributes to the same budget as policy and the delivery prefix.
        text=(ROOT/'templates/repository/standard/ENGINEERING_HARNESS.md.tpl').read_text(encoding='utf-8')
        text=text.replace('{{PROJECT_NAME}}','Qualification').replace('{{HARNESS_VERSION}}','0.19.0')
        self.assertIn('This repository uses SE Harness 0.19.0.',text)
        long=self.fixture('representative-project-'+'x'*90+'\U0001f642','0.19.0','')
        entry=long/'ENGINEERING_HARNESS.md'
        def install_root(value):
            entry.write_text(value,encoding='utf-8',newline='\n')
            lock_path=long/'.engineering-harness.lock'
            lock=json.loads(lock_path.read_text(encoding='utf-8'))
            lock['files']['ENGINEERING_HARNESS.md']['sha256']=hashlib.sha256(value.encode('utf-8')).hexdigest()
            lock_path.write_text(json.dumps(lock),encoding='utf-8')
        install_root(text)
        for host in ('codex','claude'):
            context=self.context(self.event(repo=long),host)
            self.assertTrue(context.endswith(text))
            self.assertIn('## After compaction',context)
            units=len(context.encode('utf-16-le'))//2
            self.assertGreater(units,len(context))
            self.assertLessEqual(units,delivery.MAX_CONTEXT_CHARACTERS)
            # A root that fits by itself can still overflow the FULL envelope.
            padding=delivery.MAX_CONTEXT_CHARACTERS-units+1
            oversized=text+'x'*padding
            self.assertLess(len(oversized.encode('utf-16-le'))//2,delivery.MAX_CONTEXT_CHARACTERS)
            install_root(oversized)
            refused=self.context(self.event(repo=long),host)
            self.assertIn('no truncated policy',refused)
            self.assertNotIn('## Policy / Global invariants',refused)
            install_root(text)

    def test_cli_emits_one_json_result_and_changes_no_repository_files(self):
        before={p.name:p.read_bytes() for p in self.repo.iterdir()}
        for raw in [json.dumps(self.event()).encode(),b'{"cwd":"one","cwd":"two"}',b'[]',b'{',b'x'*65537,b'['*2000+b']'*2000]:
            result=subprocess.run([sys.executable,'-I',str(SCRIPT),'--host','codex'],input=raw,capture_output=True,cwd=self.base)
            self.assertEqual(0,result.returncode,result.stderr)
            self.assertEqual(b'',result.stderr)
            output=json.loads(result.stdout)
            self.assertEqual('SessionStart',output['hookSpecificOutput']['hookEventName'])
        self.assertEqual(before,{p.name:p.read_bytes() for p in self.repo.iterdir()})

    def test_relative_paths_and_unsupported_events_refuse(self):
        for event in [self.event('pre-action'),{**self.event(),'cwd':'relative'},
                      {**self.event(),'hook_event_name':'PostToolUse'}]:
            self.assertIn('delivery is unavailable',self.context(event))

    def test_linked_entry_is_not_followed(self):
        entry=self.repo/'ENGINEERING_HARNESS.md'
        saved=self.base/'saved.md'
        saved.write_bytes(entry.read_bytes())
        entry.unlink()
        try:entry.symlink_to(saved)
        except OSError as exc:self.skipTest(f'platform cannot create test symlink: {exc}')
        self.assertIn('linked input',self.context())
