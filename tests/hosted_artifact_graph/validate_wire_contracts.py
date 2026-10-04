"""Explicit Phase 1 shape qualification; requires jsonschema==4.26.0.

Run in a disposable contract-check environment. This is not a server test and
does not add dependencies to the core harness or silently skip a missing tool.
"""

import base64
import copy
import importlib.metadata
import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource


ROOT = Path(__file__).resolve().parents[2]
FIXTURES = Path(__file__).with_name('fixtures')


def load(path):
    def unique_pairs(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f'duplicate JSON key: {key}')
            result[key] = value
        return result

    return json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=unique_pairs)


def main():
    schemas = [load(ROOT / 'server/contracts' / name)
               for name in ('remote-v1.json', 'read-v1.json', 'result-v1.json')]
    registry = Registry().with_resources((s['$id'], Resource.from_contents(s)) for s in schemas)
    for schema in schemas:
        Draft202012Validator.check_schema(schema)
    checks = []

    def check(name, schema_ref, value, expected=True):
        validator = Draft202012Validator({'$ref': schema_ref}, registry=registry, format_checker=FormatChecker())
        errors = list(validator.iter_errors(value))
        if bool(errors) == expected:
            raise AssertionError(f'{name}: expected valid={expected}; errors={[e.message for e in errors][:3]}')
        checks.append({'name': name, 'expected_valid_shape': expected, 'matched': True})

    vectors = load(FIXTURES / 'canonical-v1.json')
    wire = schemas[0]['$id'] + '#/$defs/'
    for vector in vectors['revision_vectors']:
        check(vector['name'], wire + 'StoredRevision', {k: vector[k] for k in ('revision_id', 'envelope', 'document_base64')})
    baseline = vectors['baseline_vector']['manifest']
    check('fixed-baseline', wire + 'BaselineManifest', baseline)
    manifest = load(FIXTURES / 'reference-manifest.json')
    check('full-reference-manifest', wire + 'SourceManifest', manifest)
    shared = {'schema': 'se-harness-remote-command/v1', 'project_id': baseline['project_id'],
              'operation_key': 'shape-example', 'expected_project_version': 1, 'expected_evaluator': baseline['evaluator'],
              'client': {'version': '0.22.1', 'wheel_sha256': '1' * 64}}
    context = {'context_id': 'aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa', 'expected_context_version': 0}
    command_fields = {
        'import': {'source_manifest': manifest},
        'draft-open': {'base_baseline_id': vectors['baseline_vector']['baseline_id'], 'work_order_id': 'WO-RLS-038'},
        'create-artifact': {**context, 'domain': 'hosted-artifact-graph', 'artifact_type': 'requirement', 'artifact_id': None},
        'revise-artifact': {**context, 'artifact_id': 'REQ-HAGV-001', 'expected_revision_id': vectors['revision_vectors'][0]['revision_id'],
                            'document_base64': base64.b64encode(b'synthetic shape only').decode()},
        'freeze': context,
    }
    for operation, fields in command_fields.items():
        command = {**shared, 'operation': operation, **fields}
        check(operation + '-command', wire + 'Command', command)
        bad = copy.deepcopy(command); bad['actor'] = 'mmzen'
        check(operation + '-cannot-supply-authority', wire + 'Command', bad, False)
    fixture = load(FIXTURES / 'scenarios-v1.json')
    for example in fixture['wire_examples']:
        check(example['name'], example['schema'], example['value'], example['valid_shape'])
    print(json.dumps({'kind': 'phase1-shape-check', 'jsonschema_version': importlib.metadata.version('jsonschema'),
                      'schemas_checked': len(schemas), 'checks': checks,
                      'hosted_scenarios_executed': 0,
                      'limitations': ['Shapes do not prove cross-field equality, digests, semantic admission, transaction effects, Cypher safety or live completeness.']}, indent=2))


if __name__ == '__main__':
    main()
