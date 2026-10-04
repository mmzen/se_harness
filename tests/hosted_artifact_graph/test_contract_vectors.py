"""Independent byte/reference expectations prepared before hosted serialization."""

import base64
import hashlib
import json
from pathlib import Path
import unicodedata
import unittest


ROOT = Path(__file__).resolve().parents[2]
FIXTURES = Path(__file__).with_name('fixtures')


class HostedContractVectorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.vectors = json.loads((FIXTURES / 'canonical-v1.json').read_text(encoding='utf-8'))

    def test_revision_inputs_bind_the_exact_document_and_named_scheme(self):
        for case in self.vectors['revision_vectors']:
            with self.subTest(case=case['name']):
                raw = base64.b64decode(case['document_base64'], validate=True)
                envelope = case['envelope']
                self.assertEqual(hashlib.sha256(raw).hexdigest(), envelope['document_sha256'])
                self.assertEqual(envelope, json.loads(case['canonical_utf8']))
                encoded = json.dumps(envelope, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')
                self.assertEqual(encoded, case['canonical_utf8'].encode('utf-8'))
                expected_input = case['schema'].encode('ascii') + b'\n' + encoded
                self.assertEqual(expected_input, base64.b64decode(case['hash_input_base64'], validate=True))
                self.assertEqual('sha256:' + hashlib.sha256(expected_input).hexdigest(), case['revision_id'])

    def test_body_line_endings_and_unicode_are_distinct_raw_identities(self):
        cases = {v['name'].rsplit('-', 1)[-1]: v for v in self.vectors['revision_vectors'] if v['name'].startswith('REQ-HAGV-001-')}
        selected = [v for v in self.vectors['revision_vectors'] if v['name'].startswith('REQ-HAGV-001-')]
        self.assertEqual(4, len({v['revision_id'] for v in selected}))
        lf = base64.b64decode(cases['lf']['document_base64'])
        crlf = base64.b64decode(cases['crlf']['document_base64'])
        nfd = base64.b64decode(cases['nfd']['document_base64'])
        self.assertEqual(lf, crlf.replace(b'\r\n', b'\n'))
        self.assertEqual(lf.decode(), unicodedata.normalize('NFC', nfd.decode()))
        self.assertEqual(lf, (FIXTURES / 'REQ-HAGV-001.md').read_bytes())

    def test_baseline_resolves_every_declared_edge_in_the_fixed_selection(self):
        case = self.vectors['baseline_vector']
        manifest = case['manifest']
        revisions = {v['revision_id']: v['envelope'] for v in self.vectors['revision_vectors']}
        expected = []
        for artifact_id, revision_id in manifest['selection'].items():
            envelope = revisions[revision_id]
            self.assertEqual(artifact_id, envelope['artifact_id'])
            self.assertEqual(manifest['project_id'], envelope['project_id'])
            for relation, targets in envelope['declared_relations'].items():
                expected.extend([revision_id, relation, manifest['selection'][target]] for target in targets)
        self.assertEqual(sorted(expected), manifest['resolved_relations'])
        payload = json.dumps(manifest, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()
        self.assertEqual(payload, case['canonical_utf8'].encode())
        raw = b'se-harness-artifact-baseline/v1\n' + payload
        self.assertEqual(raw, base64.b64decode(case['hash_input_base64'], validate=True))
        self.assertEqual('se-harness-artifact-baseline/v1:sha256:' + hashlib.sha256(raw).hexdigest(), case['baseline_id'])

    def test_json_preserves_sequences_and_does_not_normalize_unicode(self):
        outputs = []
        for case in self.vectors['json_vectors']:
            actual = json.dumps(case['value'], ensure_ascii=False, sort_keys=True, separators=(',', ':'))
            self.assertEqual(case['canonical_utf8'], actual)
            self.assertEqual([2, 1], json.loads(actual)['z'])
            outputs.append(actual)
        self.assertNotEqual(*outputs)

    def test_reference_manifest_fits_the_approved_import_envelope(self):
        manifest = json.loads((FIXTURES / 'reference-manifest.json').read_text(encoding='utf-8'))
        entries = manifest['artifacts']
        self.assertEqual('82f5a0ed7438a73da8f03aee23ad02a9b8cc09e1', manifest['source']['commit'])
        self.assertEqual(1909, len(entries))
        self.assertEqual(1909, len({e['artifact_id'] for e in entries}))
        self.assertEqual(sorted(e['path'] for e in entries), [e['path'] for e in entries])
        self.assertLessEqual(sum(e['bytes'] for e in entries), 64 * 1024 * 1024)
        self.assertLessEqual(max(e['bytes'] for e in entries), 1024 * 1024)
        for entry in entries:
            self.assertRegex(entry['raw_sha256'], r'^[0-9a-f]{64}$')
            self.assertRegex(entry['blob_oid'], r'^[0-9a-f]{40}$')
            self.assertNotIn('..', entry['path'].split('/'))


if __name__ == '__main__':
    unittest.main()
