"""Independent endpoint oracle from the released relationship contracts (EV-02)."""
from pathlib import Path
import unittest

from se_harness.engine.validation_core import Artifact
from se_harness.engine.validation_architecture import validate_relations

# Deliberately independent of the implementation's registry.
TYPES = ('intent', 'capability', 'requirement', 'specification', 'architecture',
         'adr', 'verification', 'work_order', 'verification_record',
         'release_contract', 'release_record', 'operating_contract', 'decision', 'risk')
EXPECTED = {
    ('capability', 'derives_from'): ('intent',),
    ('requirement', 'derives_from'): ('capability',),
    ('specification', 'specifies'): ('requirement',),
    ('architecture', 'addresses'): ('requirement',),
    ('architecture', 'conforms_to'): ('specification',),
    ('adr', 'decides'): ('architecture',),
    ('verification', 'verifies'): ('requirement',),
    ('work_order', 'implements'): ('requirement',),
    ('work_order', 'specifications'): ('specification',),
    ('work_order', 'architecture'): ('architecture', 'adr'),
    ('work_order', 'verification'): ('verification',),
    ('verification_record', 'verifies_work_order'): ('work_order',),
    ('verification_record', 'conforms_to'): ('verification',),
    ('verification_record', 'superseded_by'): ('verification_record',),
    ('release_contract', 'gates'): ('work_order',),
    ('release_record', 'satisfies'): ('release_contract',),
    ('release_record', 'includes_verification'): ('verification_record',),
    ('release_record', 'releases_work'): ('work_order',),
    ('operating_contract', 'assures'): ('requirement',),
    ('decision', 'concerns'): TYPES,
    ('decision', 'blocks'): ('requirement', 'specification', 'verification', 'architecture', 'adr', 'work_order'),
    ('decision', 'produces'): ('requirement', 'specification', 'verification', 'architecture', 'adr', 'work_order'),
    ('risk', 'threatens'): TYPES,
    ('risk', 'mitigated_by'): ('work_order',),
    ('risk', 'avoided_by'): ('adr', 'decision'),
}


class RelationPolicyTests(unittest.TestCase):
    def test_every_declared_pair_against_every_target_type(self):
        root = Path.cwd()
        for (source_type, relation), allowed in EXPECTED.items():
            for target_type in TYPES:
                with self.subTest(source=source_type, relation=relation, target=target_type):
                    source = Artifact(root / 'source.md', {'id': 'SOURCE-001', 'type': source_type,
                        'relations': {relation: ['TARGET-001']}}, '')
                    target = Artifact(root / 'target.md', {'id': 'TARGET-001', 'type': target_type}, '')
                    errors = validate_relations([source, target], root)
                    self.assertEqual(target_type not in allowed, bool(errors), errors)
                    if errors:
                        self.assertEqual({'E011'}, {e.code for e in errors})

    def test_undeclared_source_relation_is_never_an_any_type_fallback(self):
        root = Path.cwd()
        for source_type in TYPES:
            source = Artifact(root / 'source.md', {'id': 'SOURCE-001', 'type': source_type,
                'relations': {'invented': []}}, '')
            self.assertTrue(validate_relations([source], root))

    def test_shared_registry_is_complete_and_reused(self):
        from se_harness import relation_policy, preflight
        from se_harness.engine import validation_architecture
        self.assertEqual({k: set(v) for k, v in EXPECTED.items()},
                         {k: set(v) for k, v in relation_policy.RELATION_TARGET_TYPES.items()})
        self.assertIs(relation_policy.RELATION_TARGET_TYPES, validation_architecture.RELATION_TARGET_TYPES)
        self.assertIs(relation_policy.RELATION_TARGET_TYPES, preflight.RELATION_TARGET_TYPES)
