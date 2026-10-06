"""Exercise the released adapter without a store; not hosted qualification."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path
from types import SimpleNamespace

from hosted_artifact_graph.canonical import make_baseline, make_revision
from hosted_artifact_graph.evaluator import Evaluator
from hosted_artifact_graph.lifecycle import Adapter
from hosted_artifact_graph.pilot_git import encoded
from hosted_artifact_graph.protocol import EVALUATOR, Wire


def run(args):
    args.output.mkdir(parents=True, exist_ok=False)
    config = {"source_directory": str(args.source / 'source'), "source_manifest": str(args.source / 'source-manifest.json'),
              "source_inventory": str(args.source / 'source-inventory.json'), "evaluator_python": str(args.evaluator_python),
              "evaluator_wheel": str(args.evaluator_wheel)}
    evaluator = Evaluator(config)
    evaluator.identity()
    with evaluator.project() as root:
        catalog = evaluator.catalog(root)
        revisions = {i: make_revision(project_id='11111111-1111-4111-8111-111111111111', artifact_id=i,
            document=(root / item['path']).read_bytes(), original_path=item['path'],
            declared_relations=item['relations'], provenance={'kind': 'draft'}) for i, item in catalog.items()}
    service = SimpleNamespace(evaluator=evaluator, project_id='11111111-1111-4111-8111-111111111111')
    service.freeze = lambda revs, provenance: make_baseline(project_id=service.project_id, revisions=revs, provenance=provenance, evaluator=EVALUATOR)
    selected = {'view': {'kind': 'context', 'context_id': 'test', 'context_version': 0}, 'revisions': revisions}
    retained = None
    n = 0

    def act(action, inspect=False):
        nonlocal n, retained, selected
        request = {'schema': 'se-harness-lifecycle-command/v2', 'operation': 'rehearse', 'test_copy': True,
            'project_id': service.project_id, 'operation_key': 'probe-' + str(n), 'client': {'version': '0.22.2', 'wheel_sha256': '1' * 64},
            'expected_evaluator': EVALUATOR, 'expected_project_version': n, 'context_id': 'test', 'expected_context_version': n,
            'mode': 'inspect' if inspect else 'preview', 'preview_digest': None, 'action': action}
        Wire().validate(request, 'lifecycle-v2.json')
        plan = Adapter(service, request, {'id': 'probe'}, selected, retained).prepare()
        if not inspect:
            request.update(mode='apply', preview_digest=plan['result']['preview_digest'])
            plan = Adapter(service, request, {'id': 'probe'}, selected, retained).prepare()
            retained = plan['snapshot']
            selected['revisions'].update({r['envelope']['artifact_id']: r for r in plan['revisions'].values()})
            n += 1
            selected['view']['context_version'] = n
        Wire().validate(plan['result'], 'lifecycle-result-v2.json')
        (args.output / f'{n:02}-{action["kind"]}.json').write_text(json.dumps(plan['result'], indent=2) + '\n')
        print(json.dumps({'step': action['kind'], 'version': n, 'files': len(plan['result']['files'])}), flush=True)
        return plan

    def transition(ids, state, actor='test-owner'):
        return act({'kind': 'transition', 'assignments': [{'artifact': i, 'state': state, 'actor': actor,
            'reason': 'Synthetic rehearsal only; no real human decision or external authority.'} for i in ids]})

    act({'kind': 'validate'}, True)
    plan = transition(['INT-P3-001', 'CAP-P3-001', 'REQ-P3-001', 'SPEC-P3-001', 'VER-P3-001', 'REL-P3-001'], 'approved')
    base = plan['input_snapshot']['head']
    transition(['WO-P3-001'], 'approved')
    act({'kind': 'preflight', 'work_order': 'WO-P3-001', 'phase': 'start'}, True)
    transition(['WO-P3-001'], 'in_progress', 'test-executor')
    act({'kind': 'raise-risk', 'domain': 'lifecycle-pilot', 'id': 'RISK-P3-001', 'title': 'Incorrect test greeting',
         'description': 'A test implementation could return a different greeting.', 'action': 'Run the independent exact-string assertion.',
         'owner': 'test-owner', 'raised_by': 'test-executor', 'threatens': ['WO-P3-001'], 'decision_id': 'DEC-P3-001', 'recommend': 'mitigate'})
    act({'kind': 'decide', 'artifact': 'DEC-P3-001', 'decision': 'test-owner', 'reason': 'Synthetic risk treatment; no real risk acceptance.',
         'option': 'mitigate', 'disposition': 'decide', 'mitigated_by': ['WO-P3-001']})
    source = b"def greeting():\n    return 'Hello rehearsal'\n"
    # Local runner, never the service, executes the tiny fixed test source.
    namespace = {}
    exec(source, namespace)
    assert namespace['greeting']() == 'Hello rehearsal'
    evidence = b'{"test":"fixed greeting assertion","expected":"Hello rehearsal","observed":"Hello rehearsal","outcome":"passed"}\n'
    evidence_path = 'docs/engineering/lifecycle-pilot/evidence/WO-P3-001/assertion.json'
    act({'kind': 'handoff', 'work_order': 'WO-P3-001', 'from_git': base, 'files': [
        {'path': 'src/greeting.py', **encoded(source)}, {'path': evidence_path, **encoded(evidence)}]})
    transition(['WO-P3-001'], 'implemented', 'test-executor')
    act({'kind': 'capture-verification', 'id': 'VREC-P3-001', 'domain': 'lifecycle-pilot', 'work_orders': ['WO-P3-001'],
         'verifications': ['VER-P3-001'], 'evidence': [evidence_path], 'owner': 'quality-owner'})
    transition(['VREC-P3-001'], 'verified', 'quality-owner')
    act({'kind': 'prepare-release', 'id': 'RLS-P3-001', 'domain': 'lifecycle-pilot', 'release_contract': 'REL-P3-001',
         'verification_record': 'VREC-P3-001', 'work_orders': ['WO-P3-001'], 'version': '0.0.1', 'tag': 'rehearsal-0.0.1', 'owner': 'release-owner'})
    transition(['RLS-P3-001'], 'released', 'release-owner')
    act({'kind': 'check', 'artifact': 'RLS-P3-001'}, True)
    (args.output / 'snapshot.json').write_text(json.dumps(retained, indent=2) + '\n')
    print(json.dumps({'adapter_operations': n, 'hosted_scenarios_executed': 0, 'outcome': 'passed'}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--evaluator-python', type=Path, required=True)
    parser.add_argument('--evaluator-wheel', type=Path, required=True)
    run(parser.parse_args())
