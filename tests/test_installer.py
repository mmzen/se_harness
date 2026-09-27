"""Independent 0.18.0 instruction-retirement fixtures and transactional checks."""
import json
import hashlib
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from se_harness import __version__, installer
from se_harness.integrity import canonical_sha256
from se_harness.preflight import inspect_installation
from tests.fixture_support import standard_repository
from tests.mutation_guard_support import patch_mutation_authority

FIXTURES = Path(__file__).parent/'fixtures/progressive-discovery/released-0.18.0'


class InstructionMigrationTests(unittest.TestCase):
    def setUp(self):
        patch_mutation_authority(self)
        temporary = tempfile.TemporaryDirectory(prefix='instruction-migration-')
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)/'target'
        standard_repository(self.root)

    def snapshot(self):
        return {p.relative_to(self.root): p.read_bytes() for p in self.root.rglob('*') if p.is_file()}

    def prior(self, owner=b'', suffix=b'', newline=b'\n'):
        lock_path = self.root/installer.LOCK_NAME
        lock = json.loads(lock_path.read_bytes())
        lock['tool_version'] = lock['evaluator']['version'] = '0.18.0'
        lock['evaluator']['archive_name'] = 'se_harness-0.18.0-py3-none-any.whl'
        lock['evaluator']['archive_sha256'] = 'a683dbdf485d42aa20ea8502122c171a4c61c7d60f85db5b5f264bd336371c54'
        config = self.root/installer.CONFIG_NAME
        config.write_bytes(config.read_bytes().replace(__version__.encode(), b'0.18.0'))
        for name in ('AGENTS.md', 'CLAUDE.md'):
            fragment = (FIXTURES/name).read_bytes().replace(b'\n', newline)
            (self.root/name).write_bytes(owner+fragment+suffix)
            lock['files'][name] = {'mode':'fragment','sha256':canonical_sha256(fragment)}
        provenance = json.loads((FIXTURES/'provenance.json').read_bytes())
        for path in provenance['editable_guides']:
            (self.root/path).write_bytes((FIXTURES/Path(path).name).read_bytes())
        for path in list(lock['files']):
            if path.startswith('docs/engineering/harness/'):
                del lock['files'][path]
                (self.root/path).unlink()
        lock_path.write_text(json.dumps(lock),encoding='utf-8')

    def apply(self, **kwargs):
        changes, lock = installer.plan_install(self.root,project_name=None,mode='upgrade',**kwargs)
        evidence=self.delivery_fixture(changes)
        return installer.apply_changes(self.root,changes,lock,allow_updates=True,instruction_delivery_evidence=evidence,**kwargs)

    def delivery_fixture(self,changes):
        # Synthetic input for binding tests. This is not native qualification.
        root=next(item.desired for item in changes if item.path=='ENGINEERING_HARNESS.md')
        trace=self.root.parent/'synthetic-native-trace.txt'
        trace.write_bytes(b'Synthetic trace for installer boundary testing only.\n')
        digest=canonical_sha256(root)
        value={'schema':'se-harness-native-instruction-delivery-v1','repository':str(self.root.resolve()),
               'target_version':__version__,'prior_lock_sha256':canonical_sha256((self.root/installer.LOCK_NAME).read_bytes()),
               'entry_sha256':digest,'host':'claude','host_version':'fixture',
               'events':{event:{'origin':'native-host','delivered_root_sha256':digest,
                                'trace':trace.name,'trace_sha256':hashlib.sha256(trace.read_bytes()).hexdigest()}
                         for event in ('startup','compact')}}
        evidence=self.root.parent/'delivery.json'
        evidence.write_text(json.dumps(value),encoding='utf-8')
        return evidence

    def test_missing_or_stale_delivery_evidence_preserves_the_old_entry(self):
        self.prior(b'Owner\r\n')
        changes,lock=installer.plan_install(self.root,project_name=None,mode='upgrade')
        before=self.snapshot()
        with self.assertRaisesRegex(ValueError,'instruction-delivery-evidence'):
            installer.apply_changes(self.root,changes,lock,allow_updates=True)
        self.assertEqual(before,self.snapshot())
        evidence=self.delivery_fixture(changes)
        original=json.loads(evidence.read_bytes())
        for field in ('repository','prior_lock_sha256','entry_sha256','target_version'):
            with self.subTest(field=field):
                value={**original,field:'stale'}
                evidence.write_text(json.dumps(value),encoding='utf-8')
                with self.assertRaisesRegex(ValueError,'does not bind'):
                    installer.apply_changes(self.root,changes,lock,allow_updates=True,instruction_delivery_evidence=evidence)
                self.assertEqual(before,self.snapshot())
        for event in ('startup','compact'):
            value=json.loads(json.dumps(original))
            del value['events'][event]
            evidence.write_text(json.dumps(value),encoding='utf-8')
            with self.assertRaisesRegex(ValueError,'post-compaction'):
                installer.apply_changes(self.root,changes,lock,allow_updates=True,instruction_delivery_evidence=evidence)
            self.assertEqual(before,self.snapshot())
        evidence.write_text(json.dumps(original),encoding='utf-8')
        (self.root.parent/'synthetic-native-trace.txt').write_bytes(b'changed trace')
        with self.assertRaisesRegex(ValueError,'retained digest'):
            installer.apply_changes(self.root,changes,lock,allow_updates=True,instruction_delivery_evidence=evidence)
        self.assertEqual(before,self.snapshot())

    def test_fresh_install_has_no_agents_or_claude_dependency(self):
        for name in ('AGENTS.md','CLAUDE.md'):
            self.assertFalse((self.root/name).exists())
            self.assertNotIn(name,json.loads((self.root/installer.LOCK_NAME).read_bytes())['files'])
            (self.root/name).write_bytes(b'Owner bytes \xff\r\n')
        self.assertTrue(all(c.passed for c in inspect_installation(self.root)))
        self.apply()
        self.assertEqual(b'Owner bytes \xff\r\n',(self.root/'AGENTS.md').read_bytes())

    def test_recognized_fragments_preserve_all_owner_bytes(self):
        for newline, owner, suffix in [(b'\n',b'\xef\xbb\xbfOwner \xff\n',b'Tail\n'),
                                      (b'\r\n',b' \r\n\t',b'\r\n  ')]:
            with self.subTest(newline=newline):
                self.prior(owner,suffix,newline)
                lock=self.apply()
                for name in ('AGENTS.md','CLAUDE.md'):
                    self.assertEqual(owner+suffix,(self.root/name).read_bytes())
                    self.assertNotIn(name,lock['files'])
                self.assertTrue(all(c.action=='unchanged' for c in installer.plan_install(self.root,project_name=None,mode='upgrade')[0]))

    def test_harness_only_files_may_be_removed(self):
        self.prior()
        self.apply()
        self.assertFalse((self.root/'AGENTS.md').exists())
        self.assertFalse((self.root/'CLAUDE.md').exists())

    def test_custom_or_duplicate_fragment_refuses_without_writes(self):
        self.prior()
        file=self.root/'AGENTS.md'
        original=file.read_bytes()
        for changed in (original.replace(b'Read',b'Read changed',1), original+original):
            file.write_bytes(changed)
            before=self.snapshot()
            with self.assertRaises((installer.HarnessError,ValueError)):
                self.apply()
            self.assertEqual(before,self.snapshot())

    def test_unrecognized_source_version_is_not_a_recognized_migration(self):
        self.prior()
        path=self.root/installer.LOCK_NAME
        value=json.loads(path.read_bytes())
        value['tool_version']=value['evaluator']['version']='0.17.0'
        value['evaluator']['archive_name']='se_harness-0.17.0-py3-none-any.whl'
        path.write_text(json.dumps(value),encoding='utf-8')
        before=self.snapshot()
        with self.assertRaises(installer.HarnessError):self.apply()
        self.assertEqual(before,self.snapshot())

    def test_customized_seed_requires_exact_explicit_replacement(self):
        self.prior()
        path='docs/engineering/WORKFLOW.md'
        (self.root/path).write_bytes(b'Owner customized workflow\n')
        before=self.snapshot()
        with self.assertRaises(installer.HarnessError):self.apply()
        self.assertEqual(before,self.snapshot())
        self.apply(replace_files=[path])
        self.assertIn(b'Compatibility pointer',(self.root/path).read_bytes())

    def test_incomplete_replacement_collection_preserves_legacy_entry(self):
        self.prior()
        before=self.snapshot()
        original=installer.effective_template_files
        def missing(lock):
            return [item for item in original(lock) if item.target.as_posix()!='docs/engineering/harness/EXECUTE_WORK.md']
        with patch.object(installer,'effective_template_files',side_effect=missing):
            with self.assertRaisesRegex(ValueError,'required instruction file'):
                self.apply()
        self.assertEqual(before,self.snapshot())

    def test_write_failure_rolls_back_and_same_migration_can_retry(self):
        self.prior(b'Owner\r\n')
        before=self.snapshot()
        original=installer._atomic_write
        failed=False
        def interrupted(path,raw):
            nonlocal failed
            if path.name=='AGENTS.md' and not failed:
                failed=True
                raise OSError('injected write interruption')
            original(path,raw)
        with patch.object(installer,'_atomic_write',side_effect=interrupted):
            with self.assertRaisesRegex(OSError,'interruption'):self.apply()
        self.assertEqual(before,self.snapshot())
        self.apply()
        self.assertEqual(b'Owner\r\n',(self.root/'AGENTS.md').read_bytes())
