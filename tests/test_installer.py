"""Independent 0.18.0 instruction-retirement fixtures and transactional checks."""
import json
import hashlib
import contextlib
import io
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from se_harness import __version__, cli, installer
from se_harness.integrity import canonical_sha256
from se_harness.preflight import inspect_installation
from tests.fixture_support import standard_repository
from tests.mutation_guard_support import patch_mutation_authority

FIXTURES = Path(__file__).parent/'fixtures/progressive-discovery/released-0.18.0'


class MinimalInstallationTests(unittest.TestCase):
    """Independent footprint, identity, retirement and rollback boundaries."""

    def setUp(self):
        from se_harness import resources
        self.temporary = tempfile.TemporaryDirectory(prefix="minimal-install-")
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name)
        self.root = self.base / "repository"
        # Unit-only origin fixture. Packaged qualification uses the real resolver.
        origin = patch.object(resources, "_installed_resource_root", return_value=installer.template_root())
        origin.start()
        self.addCleanup(origin.stop)
        patch_mutation_authority(self)

    def files(self):
        return {p.relative_to(self.root).as_posix(): p.read_bytes()
                for p in self.root.rglob("*") if p.is_file()} if self.root.exists() else {}

    def install(self, **options):
        changes, old = installer.plan_install(self.root, project_name="Minimal", mode="init", **options)
        installer.apply_changes(self.root, changes, old, allow_updates=False, **options)
        return changes

    def prior(self):
        import zipfile
        from se_harness.evaluator_identity import canonical_payload_manifest
        from tests.fixture_support import legacy_repository
        legacy_repository(self.root, "Minimal")
        self.wheel = self.base / f"se_harness-{__version__}-py3-none-any.whl"
        source = Path(__file__).resolve().parents[1]
        with zipfile.ZipFile(self.wheel, "w") as archive:
            for member in json.loads(canonical_payload_manifest())["files"]:
                relative = member["path"]
                name = relative if relative.startswith("se_harness/") else (
                    f"se_harness-{__version__}.data/data/share/se-harness/" + relative)
                archive.write(source / relative, name)
        return dict(external_resources=True, prior_wheel=self.wheel)

    def delivery(self, changes):
        config = next(c.desired for c in changes if c.path == installer.CONFIG_NAME)
        lock = json.loads(next(c.desired for c in changes if c.path == installer.LOCK_NAME))
        entry = installer._replacement_resources(self.root, config, lock)
        # Binding fixture only; this does not claim native host delivery.
        trace = self.base / "synthetic-trace.txt"
        trace.write_bytes(b"Unit binding fixture; not native qualification.\n")
        digest = canonical_sha256(entry)
        value = {"schema": "se-harness-native-instruction-delivery-v1",
                 "repository": str(self.root.resolve()), "target_version": __version__,
                 "prior_lock_sha256": canonical_sha256((self.root / installer.LOCK_NAME).read_bytes()),
                 "entry_sha256": digest, "host": "codex", "host_version": "unit-fixture",
                 "events": {event: {"origin": "native-host", "delivered_root_sha256": digest,
                                   "trace": trace.name, "trace_sha256": hashlib.sha256(trace.read_bytes()).hexdigest()}
                            for event in ("startup", "compact")}}
        path = self.base / "delivery.json"
        path.write_text(json.dumps(value), encoding="utf-8")
        return path

    def test_default_footprint_repeat_and_owner_bytes(self):
        self.root.mkdir()
        (self.root / "AGENTS.md").write_bytes(b"Owner\xff\r\n")
        (self.root / "CLAUDE.md").write_bytes(b"Claude owner\r\n")
        before = self.files()
        changes, old = installer.plan_install(self.root, project_name="Minimal", mode="init")
        self.assertEqual(before, self.files())
        self.assertEqual({installer.CONFIG_NAME, installer.LOCK_NAME}, {c.path for c in changes})
        installer.apply_changes(self.root, changes, old, allow_updates=False)
        after = self.files()
        self.assertEqual({installer.CONFIG_NAME, installer.LOCK_NAME}, set(after) - set(before))
        self.assertTrue(all(after[p] == raw for p, raw in before.items()))
        repeat = self.install()
        self.assertTrue(all(c.action == "unchanged" for c in repeat))
        self.assertEqual(after, self.files())
        self.assertEqual({}, json.loads(after[installer.LOCK_NAME])["files"])
        self.assertNotIn(b"\r", after[installer.LOCK_NAME])

    def test_optional_integrations_are_explicit_and_preserve_owner_content(self):
        self.install(integrations=["git", "pr"])
        self.assertEqual({installer.CONFIG_NAME, installer.LOCK_NAME, ".gitattributes",
                          ".github/PULL_REQUEST_TEMPLATE.md"}, set(self.files()))
        self.assertNotIn(".gitignore", self.files())
        self.assertFalse((self.root / "ENGINEERING_HARNESS.md").exists())

    def test_source_without_installed_resources_refuses_without_writes(self):
        from se_harness.resources import _installed_resource_root, ResourceError
        with patch("se_harness.resources._installed_resource_root",
                   side_effect=ResourceError("external resources require an installed evaluator wheel")):
            with self.assertRaisesRegex(ResourceError, "installed evaluator"):
                self.install()
        self.assertEqual({}, self.files())

    def test_changed_preview_refuses_without_partial_writes(self):
        changes, old = installer.plan_install(self.root, project_name="Minimal", mode="init")
        self.root.mkdir()
        (self.root / installer.CONFIG_NAME).write_bytes(b"owner content")
        before = self.files()
        with self.assertRaisesRegex(installer.HarnessError, "plan changed"):
            installer.apply_changes(self.root, changes, old, allow_updates=False)
        self.assertEqual(before, self.files())

    def test_linked_parent_refuses_without_writes(self):
        outside = self.base / "outside"
        outside.mkdir()
        self.root.mkdir()
        try:
            (self.root / ".github").symlink_to(outside, target_is_directory=True)
        except OSError:
            self.skipTest("host cannot create symlinks")
        with self.assertRaisesRegex(ValueError, "linked|symlink"):
            installer.plan_install(self.root, project_name="Minimal", mode="init", integrations=["pr"])
        self.assertEqual([], list(outside.iterdir()))
        self.assertFalse((self.root / installer.CONFIG_NAME).exists())

    def test_removed_owner_integration_stays_removed_unless_explicitly_selected(self):
        self.install(integrations=iter(["pr"]))
        path = self.root / ".github/PULL_REQUEST_TEMPLATE.md"
        path.unlink()
        changes, old = installer.plan_install(self.root, project_name=None, mode="upgrade")
        self.assertEqual("unchanged", next(c.action for c in changes if c.path.endswith("PULL_REQUEST_TEMPLATE.md")))
        installer.apply_changes(self.root, changes, old, allow_updates=True)
        self.assertFalse(path.exists())
        changes, old = installer.plan_install(self.root, project_name=None, mode="upgrade", integrations=["pr"])
        installer.apply_changes(self.root, changes, old, allow_updates=True, integrations=["pr"])
        self.assertTrue(path.is_file())

    def test_retirement_cannot_silently_ignore_a_retained_integration(self):
        options = self.prior()
        before = self.files()
        with self.assertRaisesRegex(installer.HarnessError, "prior editable seed"):
            installer.plan_install(self.root, project_name=None, mode="upgrade",
                                   retire_files=[".github/PULL_REQUEST_TEMPLATE.md"], **options)
        self.assertEqual(before, self.files())

    def test_prior_wheel_is_one_snapshot_even_if_original_changes_after_hashing(self):
        from se_harness.evaluator_identity import wheel_payload_sha256
        options = self.prior()

        def replace_original(snapshot, version):
            digest = wheel_payload_sha256(snapshot, version)
            self.wheel.write_bytes(b"replaced original")
            return digest

        with patch("se_harness.evaluator_identity.wheel_payload_sha256", side_effect=replace_original):
            changes, _ = installer.plan_install(self.root, project_name=None, mode="upgrade", **options)
        self.assertEqual("remove", next(c.action for c in changes if c.path == "ENGINEERING_HARNESS.md"))
        # Apply re-plans against the now-invalid input and must refuse without writes.
        before = self.files()
        with self.assertRaises(ValueError):
            installer.plan_install(self.root, project_name=None, mode="upgrade", **options)
        self.assertEqual(before, self.files())

    def test_migration_requires_delivery_and_explicit_stock_seed_selection(self):
        options = self.prior()
        before = self.files()
        changes, old = installer.plan_install(self.root, project_name=None, mode="upgrade", **options)
        authoring = "docs/engineering/ARTIFACT_AUTHORING.md"
        self.assertEqual("preserve", next(c.action for c in changes if c.path == authoring))
        with self.assertRaisesRegex(ValueError, "instruction-delivery-evidence"):
            installer.apply_changes(self.root, changes, old, allow_updates=True, **options)
        self.assertEqual(before, self.files())
        options["retire_files"] = [authoring]
        changes, old = installer.plan_install(self.root, project_name=None, mode="upgrade", **options)
        installer.apply_changes(self.root, changes, old, allow_updates=True,
                                instruction_delivery_evidence=self.delivery(changes), **options)
        after = self.files()
        self.assertNotIn("ENGINEERING_HARNESS.md", after)
        self.assertNotIn(authoring, after)
        preserved_template = "docs/engineering/templates/WORK_ORDER.template.md"
        self.assertEqual(before[preserved_template], after[preserved_template])
        self.assertEqual(5, json.loads(after[installer.LOCK_NAME])["schema"])
        replay, _ = installer.plan_install(self.root, project_name=None, mode="upgrade")
        self.assertTrue(all(c.action == "unchanged" for c in replay))

    def test_customized_seed_and_wrong_prior_wheel_refuse_before_writes(self):
        options = self.prior()
        authoring = self.root / "docs/engineering/ARTIFACT_AUTHORING.md"
        authoring.write_bytes(authoring.read_bytes() + b"\nOwner instructions\n")
        before = self.files()
        changes, old = installer.plan_install(self.root, project_name=None, mode="upgrade", **options)
        self.assertEqual("customized", next(c.action for c in changes if c.path.endswith("ARTIFACT_AUTHORING.md")))
        with self.assertRaisesRegex(installer.HarnessError, "customizations"):
            installer.apply_changes(self.root, changes, old, allow_updates=True, **options)
        self.assertEqual(before, self.files())
        self.wheel.write_bytes(b"not a wheel")
        with self.assertRaises(ValueError):
            installer.plan_install(self.root, project_name=None, mode="upgrade", **options)
        self.assertEqual(before, self.files())

    def test_migration_rolls_back_after_removal_and_can_retry(self):
        options = self.prior()
        changes, old = installer.plan_install(self.root, project_name=None, mode="upgrade", **options)
        delivery = self.delivery(changes)
        before = self.files()
        write = installer._atomic_write
        failed = False

        def interrupt(path, content):
            nonlocal failed
            if path.name == installer.LOCK_NAME and not failed:
                failed = True
                raise OSError("injected interruption after retirement")
            write(path, content)

        with patch.object(installer, "_atomic_write", side_effect=interrupt):
            with self.assertRaisesRegex(OSError, "injected interruption"):
                installer.apply_changes(self.root, changes, old, allow_updates=True,
                                        instruction_delivery_evidence=delivery, **options)
        self.assertTrue(failed)
        self.assertEqual(before, self.files())
        installer.apply_changes(self.root, changes, old, allow_updates=True,
                                instruction_delivery_evidence=delivery, **options)
        self.assertFalse((self.root / "ENGINEERING_HARNESS.md").exists())


class InstructionMigrationFixture(unittest.TestCase):
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
            # The fixture may already have CRLF in a Windows checkout.
            # Normalize first so this case supplies CRLF, not CR-CR-LF.
            fragment = (FIXTURES/name).read_bytes().replace(b'\r\n', b'\n').replace(b'\n', newline)
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


class InstructionMigrationTests(InstructionMigrationFixture):
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

    def test_upgrade_cli_reports_delivery_refusal_without_writes(self):
        self.prior(b'Owner\r\n')
        changes, _ = installer.plan_install(self.root, project_name=None, mode='upgrade')
        evidence = self.delivery_fixture(changes)
        stale = json.loads(evidence.read_bytes())
        stale['entry_sha256'] = '0' * 64
        evidence.write_text(json.dumps(stale), encoding='utf-8')
        before = self.snapshot()
        cases = [
            ([], 'requires --instruction-delivery-evidence'),
            (['--instruction-delivery-evidence', str(evidence)], 'does not bind'),
        ]
        for arguments, diagnostic in cases:
            with self.subTest(arguments=arguments):
                stdout, stderr = io.StringIO(), io.StringIO()
                with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                    code = cli.main(['upgrade', str(self.root), '--apply', '--json', *arguments])
                self.assertEqual(2, code)
                self.assertIn('harnessctl: ', stderr.getvalue())
                self.assertIn(diagnostic, stderr.getvalue())
                self.assertNotIn('Traceback', stderr.getvalue())
                self.assertEqual('', stdout.getvalue())
                self.assertEqual(before, self.snapshot())

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


class RetiredGuideTests(InstructionMigrationFixture):
    """Expected predecessor text comes from the retained public wheel, not the renderer."""

    RELEASED = FIXTURES.parent / 'released-0.19.0'
    NAMES = ('OPERATING_CARD.md', 'DECISION_RIGHTS.md', 'QUALITY_GATES.md',
             'WORKFLOW.md', 'TRACEABILITY.md', 'TECHNICAL_COMMUNICATION.md')

    def test_new_install_omits_all_six_guides_and_keeps_current_instructions(self):
        lock = json.loads((self.root / installer.LOCK_NAME).read_bytes())
        distributed = {item.target.as_posix() for item in installer.template_files()}
        for name in self.NAMES:
            relative = 'docs/engineering/' + name
            self.assertFalse((self.root / relative).exists(), name)
            self.assertNotIn(relative, lock['files'])
            self.assertNotIn(relative, distributed)
        self.assertTrue(all(c.passed for c in inspect_installation(self.root)))

    def test_published_pointer_fixture_digests_match(self):
        provenance = json.loads((self.RELEASED / 'provenance.json').read_bytes())
        self.assertEqual(set(self.NAMES), set(provenance['files']))
        for name, entry in provenance['files'].items():
            raw = (self.RELEASED / name).read_bytes().replace(b'\r\n', b'\n')
            self.assertEqual(entry['sha256'], hashlib.sha256(raw).hexdigest(), name)

    def test_current_owner_seeds_preserve_stock_custom_and_absent_bytes(self):
        lock_path = self.root / installer.LOCK_NAME
        lock = json.loads(lock_path.read_bytes())
        lock['tool_version'] = lock['evaluator']['version'] = '0.19.0'
        observed = {}
        for i, name in enumerate(self.NAMES):
            relative = 'docs/engineering/' + name
            raw = (self.RELEASED / name).read_bytes()
            if i % 3 == 1:
                raw += b'\r\nOwner note \xff\r\n'
            if i % 3 == 2:
                raw = None
            if raw is not None:
                (self.root / relative).write_bytes(raw)
            lock['files'][relative] = {'mode': 'seed', 'state': 'removed' if raw is None else 'present'}
            observed[relative] = raw
        lock_path.write_text(json.dumps(lock), encoding='utf-8')
        result = self.apply()
        for relative, raw in observed.items():
            self.assertNotIn(relative, result['files'])
            self.assertEqual(raw, (self.root / relative).read_bytes() if (self.root / relative).exists() else None)
        self.assertTrue(all(c.passed for c in inspect_installation(self.root)))
        before = self.snapshot()
        self.apply()
        self.assertEqual(before, self.snapshot())

    def test_018_preview_and_conversion_match_published_pointers_without_tracking_them(self):
        self.prior(b'Owner\r\n')
        changes, _ = installer.plan_install(self.root, project_name=None, mode='upgrade')
        by_path = {item.path: item for item in changes}
        for name in self.NAMES:
            expected = (self.RELEASED / name).read_bytes().replace(b'\r\n', b'\n')
            item = by_path['docs/engineering/' + name]
            self.assertEqual('update', item.action)
            self.assertEqual(expected, item.desired)
        lock = self.apply()
        for name in self.NAMES:
            relative = 'docs/engineering/' + name
            self.assertEqual((self.RELEASED / name).read_bytes().replace(b'\r\n', b'\n'), (self.root / relative).read_bytes())
            self.assertNotIn(relative, lock['files'])
        self.assertTrue(all(c.passed for c in inspect_installation(self.root)))

    def test_unsafe_retired_destination_refuses_before_any_write(self):
        path = self.root / 'docs/engineering/OPERATING_CARD.md'
        path.mkdir()
        before = self.snapshot()
        with self.assertRaises((installer.HarnessError, OSError)):
            self.apply()
        self.assertEqual(before, self.snapshot())
