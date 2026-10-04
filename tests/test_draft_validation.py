"""SPEC-HAG-004: expectations fixed before the classifier implementation."""
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock

from se_harness.engine.validate_engineering_artifacts import validate_repository
from tests.artifact_support import formal, write
from tests.cli_support import invoke
from tests.fixture_support import standard_repository
from tests.mutation_guard_support import patch_mutation_authority

SUPPORTED = {
    'intent': 'INT', 'capability': 'CAP', 'requirement': 'REQ',
    'specification': 'SPEC', 'architecture': 'ARCH', 'adr': 'ADR',
    'verification': 'VER', 'work_order': 'WO', 'release_contract': 'REL',
    'operating_contract': 'OPS',
}


class DraftValidationTests(unittest.TestCase):
    def setUp(self):
        patch_mutation_authority(self)
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name) / 'repository'
        standard_repository(self.root)
        self.selected = self.root / 'docs/engineering/demo/requirements/REQ-DEMO-001.md'
        write(self.root / 'docs/engineering/demo/capabilities/CAP-DEMO-001.md',
              formal('CAP-DEMO-001', 'capability', 'draft', {}))
        write(self.root / 'docs/engineering/demo/releases/RLS-DEMO-001.md',
              formal('RLS-DEMO-001', 'release_record', 'draft', {}))
        self.requirement()

    def requirement(self, targets=None, extra='', relations=None):
        text = formal('REQ-DEMO-001', 'requirement', 'draft',
            relations if relations is not None else {'derives_from': ['CAP-DEMO-001'] if targets is None else targets},
            'statement = "An observable behavior."\nverification_method = ["test"]\n' + extra)
        write(self.selected, text)

    def snapshot(self):
        return {p.relative_to(self.root).as_posix(): p.read_bytes()
                for p in self.root.rglob('*') if p.is_file()}

    def query(self, artifact='REQ-DEMO-001', expected=True):
        before = self.snapshot()
        code, output, error = invoke('validate-draft', str(self.root), '--artifact', artifact, '--json')
        self.assertEqual(0 if expected else 1, code, error or output)
        data = json.loads(output, parse_constant=self.fail)
        self.assertEqual('se-harness-draft-validation-v1', data['schema'])
        self.assertEqual(expected, data['admissible'])
        self.assertEqual(before, self.snapshot())
        self.assertNotIn('next', data)
        return data

    def test_all_generated_templates_are_admissible_and_explicitly_incomplete(self):
        for kind, prefix in SUPPORTED.items():
            with self.subTest(kind=kind):
                identifier = prefix + '-GENERATED-001'
                code, output, error = invoke('create-artifact', str(self.root), '--domain', 'demo',
                    '--type', kind, '--id', identifier)
                self.assertEqual(0, code, error or output)
                data = self.query(identifier)
                self.assertTrue(data['incomplete'], data)
                self.assertEqual(kind, data['selection']['type'])

    def test_missing_empty_and_exact_placeholder_links(self):
        for relations in ({}, {'derives_from': []}, {'derives_from': ['CAP-xxx']}):
            with self.subTest(relations=relations):
                self.requirement(relations=relations)
                data = self.query()
                self.assertTrue(any(f.get('relation') == 'derives_from' for f in data['incomplete']))
                report = validate_repository(self.root)
                self.assertTrue(any(e.path.endswith('REQ-DEMO-001.md') for e in report.errors))

    def test_complete_requirement_and_background_are_distinct(self):
        data = self.query()
        self.assertEqual([], data['incomplete'])
        self.assertTrue(data['background'])
        self.assertEqual('docs/engineering/demo/requirements/REQ-DEMO-001.md', data['selection']['path'])

    def test_invalid_edges_and_mixed_placeholder_cannot_hide_errors(self):
        for targets in (['RLS-DEMO-001'], ['CAP-xxx', 'RLS-DEMO-001'], ['CAP-MISSING-999'],
                        [''], [42], 'CAP-DEMO-001', ['REQ-DEMO-001'], ['INT-xxx']):
            with self.subTest(targets=targets):
                self.requirement(relations={'derives_from': targets})
                data = self.query(expected=False)
                self.assertTrue(any(f.get('relation') == 'derives_from' for f in data['errors']))
                if targets == ['CAP-xxx', 'RLS-DEMO-001']:
                    self.assertTrue(data['incomplete'])
                    self.assertTrue(any(f.get('target') == 'RLS-DEMO-001' for f in data['errors']))
        self.requirement(relations={'concerns': ['CAP-xxx']})
        self.query(expected=False)

    def test_non_array_and_toml_date_targets_produce_structured_refusals(self):
        for value in ('"CAP-DEMO-001"', '42', '[2026-01-01]', '[{}]', '[nan]', '[inf]', '[{bad=nan}]'):
            self.requirement()
            write(self.selected, self.selected.read_text().replace('derives_from = ["CAP-DEMO-001"]',
                                                                  'derives_from = ' + value))
            result = self.query(expected=False)
            self.assertTrue(any(e.get('relation') == 'derives_from' for e in result['errors']))

    def test_one_placeholder_does_not_exempt_other_metadata_fields(self):
        for kind, prefix, old, new in (
            ('work_order', 'WO', '"<required or not_required>"', '"sometimes"'),
            ('work_order', 'WO', '"<why future decisions do or do not require commit-bound assurance>"', '42'),
            ('work_order', 'WO', '"<exact/repository-relative/path>"', '"../escape.py"'),
            ('architecture', 'ARCH', 'triggers = []', 'triggers = ["invented"]'),
            ('architecture', 'ARCH', '"<adr_required-or-no_significant_decision>"', '"<required or not_required>"'),
            ('release_contract', 'REL', '"<full commit id, 40 or 64 hex>"', '"not-a-commit"'),
        ):
            with self.subTest(kind=kind, value=new):
                identifier = prefix + '-SHAPE-001'
                code, output, error = invoke('create-artifact', str(self.root), '--domain', 'demo',
                                             '--type', kind, '--id', identifier)
                paths = list((self.root / 'docs/engineering/demo').rglob(identifier + '.md'))
                # Reuse the same canonical source between cases, without relying on the classifier.
                if code != 0:
                    self.assertEqual(1, len(paths), error or output)
                path = paths[0]
                original = path.read_text()
                self.assertIn(old, original)
                write(path, original.replace(old, new))
                result = self.query(identifier, expected=False)
                self.assertTrue(result['incomplete'])
                self.assertTrue(any(e.get('field') for e in result['errors']))
                write(path, original)

    def test_modified_repository_template_cannot_grant_a_new_exception(self):
        template = self.root / 'docs/engineering/templates/REQUIREMENT.template.md'
        write(template, template.read_text().replace('CAP-xxx', 'RLS-DEMO-001'))
        self.requirement(['RLS-DEMO-001'])
        self.query(expected=False)

    def test_ordinary_validation_rejects_unlinked_requirement_to_release(self):
        self.requirement(['RLS-DEMO-001'])
        data = self.query(expected=False)
        self.assertIn('E011', {e['code'] for e in data['errors']})
        report = validate_repository(self.root)
        self.assertTrue(any(e.code == 'E011' and e.path.endswith('REQ-DEMO-001.md') for e in report.errors))

    def test_identity_dates_status_and_protected_metadata_refuse(self):
        self.requirement()
        original = self.selected.read_text()
        replacements = [
            ('type = "requirement"', 'type = "capability"'),
            ('type = "requirement"', 'type = "unknown"'),
            ('id = "REQ-DEMO-001"\n', ''),
            ('status = "draft"', 'status = "approved"'),
            ('created = "2026-08-11"', 'created = "2026-02-30"'),
            ('updated = "2026-08-11"', 'updated = "YYYY-MM-DD"'),
            ('owners = ["owner"]', 'owners = 42'),
            ('[relations]', 'lifecycle_events = []\n[relations]'),
            ('[relations]', 'disposition = {}\n[relations]'),
            ('[relations]', 'relations = 42\n[ignored]'),
            ('statement = "An observable behavior."', 'statement = []'),
            ('verification_method = ["test"]', 'verification_method = [42]'),
        ]
        for old, new in replacements:
            with self.subTest(new=new):
                write(self.selected, original.replace(old, new))
                self.query(expected=False)

    def test_unknown_and_unsupported_selection_refuse(self):
        self.query('REQ-UNKNOWN-001', expected=False)
        for kind, prefix in [('decision', 'DEC'), ('risk', 'RISK'), ('verification_record', 'VREC'), ('release_record', 'RLS')]:
            identifier = prefix + '-UNSUPPORTED-001'
            write(self.root / ('docs/engineering/demo/' + identifier + '.md'), formal(identifier, kind, 'draft', {}))
            self.query(identifier, expected=False)

    def test_catalog_parse_and_duplicate_failures_block_even_if_unrelated(self):
        bad = self.root / 'docs/engineering/demo/bad.md'
        for text in ('+++\nid = [\n+++', '+++\nid="X"\nid="Y"\n+++',
                     formal('CAP-DEMO-001', 'capability', 'draft', {})):
            with self.subTest(text=text):
                write(bad, text)
                data = self.query(expected=False)
                self.assertTrue(any(e['path'].endswith('bad.md') or e['code'] == 'E003' for e in data['errors']))

    def test_determinism_cli_text_and_usage(self):
        first = self.query()
        self.assertEqual(first, self.query())
        code, output, error = invoke('validate-draft', str(self.root), '--artifact', 'REQ-DEMO-001')
        self.assertEqual(0, code, error)
        self.assertIn('REQ-DEMO-001', output)
        self.assertIn('background', output.lower())
        self.assertEqual(2, invoke('validate-draft', str(self.root))[0])
        self.assertEqual(2, invoke('validate-draft', str(self.root / 'absent'), '--artifact', 'REQ-DEMO-001')[0])

    def test_projection_catalog_is_parsed_only_once(self):
        from se_harness import draft_validation
        with mock.patch.object(draft_validation, 'load_artifacts', wraps=draft_validation.load_artifacts) as load:
            self.query()
            self.assertEqual(1, load.call_count)

    def test_draft_admission_does_not_grant_approval(self):
        self.requirement(['CAP-xxx'])
        self.query()
        before = self.snapshot()
        code, output, error = invoke('transition', str(self.root), '--set', 'REQ-DEMO-001=approved',
                                     '--decision', 'REQ-DEMO-001=operator', '--json')
        self.assertNotEqual(0, code)
        self.assertEqual(before, self.snapshot())
