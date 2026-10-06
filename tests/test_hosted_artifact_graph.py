"""Independent SPEC-HAG-001 byte contracts; these are not hosted scenarios."""
from __future__ import annotations

import base64
import copy
import json
from pathlib import Path
import unittest

from server.hosted_artifact_graph.canonical import (
    BASELINE_SCHEME, CanonicalError, canonical_json, decode_json, make_baseline,
    make_revision, named_digest, verify_revision,
)
from tests.hosted_artifact_graph.test_contract_vectors import HostedContractVectorTests

__all__ = ["HostedContractVectorTests", "HostedCanonicalTests"]

FIXTURES = Path(__file__).parent / "hosted_artifact_graph" / "fixtures"


class HostedCanonicalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.vectors = json.loads((FIXTURES / "canonical-v1.json").read_text(encoding="utf-8"))

    def revision(self, vector):
        e = vector["envelope"]
        return make_revision(project_id=e["project_id"], artifact_id=e["artifact_id"],
                             document=base64.b64decode(vector["document_base64"]),
                             declared_relations=e["declared_relations"], provenance=e["provenance"],
                             original_path=e["original_path"])

    def baseline(self, revisions=None):
        expected = self.vectors["baseline_vector"]["manifest"]
        if revisions is None:
            revisions = {v["envelope"]["artifact_id"]: self.revision(v)
                         for v in self.vectors["revision_vectors"][:3]}
        return make_baseline(project_id=expected["project_id"], revisions=revisions,
                             evaluator=expected["evaluator"], provenance=expected["provenance"])

    def test_all_independently_fixed_revision_bytes_and_hashes(self):
        for vector in self.vectors["revision_vectors"]:
            with self.subTest(vector=vector["name"]):
                actual = self.revision(vector)
                self.assertEqual(vector["revision_id"], actual["revision_id"])
                self.assertEqual(vector["document_base64"], actual["document_base64"])
                self.assertEqual(vector["canonical_utf8"].encode(), canonical_json(actual["envelope"]))
                raw = vector["schema"].encode() + b"\n" + canonical_json(actual["envelope"])
                self.assertEqual(base64.b64decode(vector["hash_input_base64"]), raw)
                self.assertEqual(actual, verify_revision(actual))

    def test_independent_baseline_manifest_and_hash(self):
        vector = self.vectors["baseline_vector"]
        actual = self.baseline()
        self.assertEqual(vector["manifest"], actual["manifest"])
        self.assertEqual(vector["baseline_id"], actual["baseline_id"])
        self.assertEqual(vector["canonical_utf8"].encode(), canonical_json(actual["manifest"]))
        self.assertEqual(base64.b64decode(vector["hash_input_base64"]),
                         BASELINE_SCHEME.encode() + b"\n" + canonical_json(actual["manifest"]))

    def test_unicode_forms_and_sequences_are_not_normalized(self):
        for vector in self.vectors["json_vectors"]:
            self.assertEqual(vector["canonical_utf8"].encode(), canonical_json(vector["value"]))
        self.assertNotEqual(canonical_json([1, 2]), canonical_json([2, 1]))
        ids = [self.revision(v)["revision_id"] for v in self.vectors["revision_vectors"][2:]]
        self.assertEqual(len(ids), len(set(ids)))

    def test_semantic_relation_sets_are_normalized_without_modifying_inputs(self):
        vector = copy.deepcopy(self.vectors["revision_vectors"][2])
        targets = vector["envelope"]["declared_relations"]["derives_from"]
        targets += targets
        actual = self.revision(vector)
        self.assertEqual(self.vectors["revision_vectors"][2]["revision_id"], actual["revision_id"])
        self.assertEqual(2, len(targets))
        vector["envelope"]["provenance"]["principal_id"] = "different"
        self.assertEqual("author-a", actual["envelope"]["provenance"]["principal_id"])

    def test_later_revision_does_not_modify_existing_baseline_value(self):
        old = self.baseline()
        snapshot = canonical_json(old)
        revisions = {v["envelope"]["artifact_id"]: self.revision(v)
                     for v in self.vectors["revision_vectors"][:3]}
        revisions["REQ-HAGV-001"] = self.revision(self.vectors["revision_vectors"][-1])
        changed = self.baseline(revisions)
        self.assertNotEqual(old["baseline_id"], changed["baseline_id"])
        self.assertEqual(snapshot, canonical_json(old))

    def test_json_decode_rejects_ambiguous_or_unsupported_inputs(self):
        for raw in (b'{"a":1,"a":2}', b'{"outer":{"x":1,"x":2}}', b'1.0', b'1e2',
                    b'NaN', b'Infinity', b'-Infinity', b'"\\ud800"', b'\xff', b'\xef\xbb\xbf{}'):
            with self.subTest(raw=raw), self.assertRaises(CanonicalError):
                decode_json(raw, max_bytes=100)
        self.assertEqual({"x": [True, 1, None]}, decode_json(b'{"x":[true,1,null]}', max_bytes=100))

    def test_decode_enforces_bytes_before_parsing(self):
        self.assertEqual({}, decode_json(b'{}', max_bytes=2))
        for raw, limit in ((b'{}', 1), (b'{}', -1), (b'{}', True), ('{}', 2)):
            with self.subTest(raw=raw, limit=limit), self.assertRaises(CanonicalError):
                decode_json(raw, max_bytes=limit)

    def test_encoder_rejects_values_without_canonical_json_meaning(self):
        circular = []
        circular.append(circular)
        for value in (1.0, float('nan'), {1: 'x'}, (1, 2), {1, 2}, b'bytes', '\ud800', circular):
            with self.subTest(kind=type(value).__name__), self.assertRaises(CanonicalError):
                canonical_json(value)

    def test_digest_scheme_is_part_of_identity(self):
        self.assertNotEqual(named_digest('scheme-a', {}), named_digest('scheme-b', {}))
        with self.assertRaises(CanonicalError):
            named_digest('scheme\nextra', {})

    def test_document_byte_limit_and_utf8(self):
        v = copy.deepcopy(self.vectors["revision_vectors"][0])
        for raw in (b'\xff', b'a' * (1024 * 1024 + 1)):
            v["document_base64"] = base64.b64encode(raw).decode()
            with self.assertRaises(CanonicalError):
                self.revision(v)
        v["document_base64"] = base64.b64encode(b'a' * (1024 * 1024)).decode()
        self.assertTrue(self.revision(v)["revision_id"].startswith('sha256:'))

    def test_original_path_rejects_escape_and_preserves_valid_bytes(self):
        v = copy.deepcopy(self.vectors["revision_vectors"][0])
        for path in ('', '/a', '../a', 'a/../b', 'a/./b', 'a//b', 'a/', 'C:/x', 'a\\b', 'a\x00b'):
            v["envelope"]["original_path"] = path
            with self.subTest(path=path), self.assertRaises(CanonicalError):
                self.revision(v)
        v["envelope"]["original_path"] = 'docs/engineering/a.md'
        self.assertEqual('docs/engineering/a.md', self.revision(v)["envelope"]["original_path"])

    def test_stored_revision_tampering_is_refused(self):
        original = self.revision(self.vectors["revision_vectors"][0])
        variants = []
        for key, value in (('revision_id', 'sha256:' + '0' * 64), ('document_base64', 'eA=='),
                           ('document_base64', 'eB=='), ('document_base64', 'eA==\n')):
            changed = copy.deepcopy(original)
            changed[key] = value
            variants.append(changed)
        for key in ('schema', 'document_sha256', 'artifact_id'):
            changed = copy.deepcopy(original)
            changed['envelope'][key] = 'tampered'
            variants.append(changed)
        changed = copy.deepcopy(original)
        changed['envelope']['extra'] = 'ignored?'
        variants.append(changed)
        for changed in variants:
            with self.assertRaises(CanonicalError):
                verify_revision(changed)

    def test_baseline_refuses_missing_target_cross_project_and_wrong_artifact(self):
        vectors = self.vectors["revision_vectors"]
        revisions = {v["envelope"]["artifact_id"]: self.revision(v) for v in vectors[:3]}
        del revisions['CAP-HAGV-001']
        with self.assertRaisesRegex(CanonicalError, 'unresolved'):
            self.baseline(revisions)
        cross = copy.deepcopy(vectors[0])
        cross['envelope']['project_id'] = '00000000-0000-4000-8000-000000000099'
        with self.assertRaisesRegex(CanonicalError, 'project and artifact'):
            self.baseline({'INT-HAGV-001': self.revision(cross)})
        with self.assertRaisesRegex(CanonicalError, 'project and artifact'):
            self.baseline({'WRONG-ID': self.revision(vectors[0])})


if __name__ == '__main__':
    unittest.main()
