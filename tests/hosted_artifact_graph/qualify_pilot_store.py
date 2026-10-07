"""Real Memgraph fault and competing-writer tests; run in the packaged service."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from hosted_artifact_graph.canonical import canonical_json
from hosted_artifact_graph.protocol import Refusal
from hosted_artifact_graph.service import Service


def fingerprint(service):
    with service.store.transaction() as tx:
        nodes = [dict(r) for r in tx.run('MATCH (n) RETURN labels(n) AS labels, properties(n) AS properties')]
        edges = [dict(r) for r in tx.run('MATCH (a)-[e]->(b) RETURN labels(a) AS al, properties(a) AS a, type(e) AS kind, properties(e) AS e, labels(b) AS bl, properties(b) AS b')]
        version = service.store.project(tx)['command_version']
    digest = hashlib.sha256(canonical_json([sorted(nodes, key=canonical_json), sorted(edges, key=canonical_json)])).hexdigest()
    return {'project_version': version, 'nodes': len(nodes), 'edges': len(edges), 'sha256': digest}


def run(args):
    service = Service(json.loads(args.config.read_text()), json.loads(args.credentials.read_text()))
    principal = next(p for p in service.credentials['principals'] if p['id'] == 'operator')
    state = json.loads(args.state.read_text())
    events = []
    template = copy.deepcopy(state['last_request'])
    template.update(expected_project_version=state['project_version'],
                    expected_context_version=state['context']['context_version'])

    def save():
        args.output.write_text(json.dumps({'state': 'running', 'events': events}, indent=2) + '\n')

    def request(key, action):
        value = copy.deepcopy(template)
        value.update(operation_key=key, action=action, mode='preview', preview_digest=None)
        return value

    def preview(value):
        result = service.rehearse(principal, value)
        applied = copy.deepcopy(value)
        applied.update(mode='apply', preview_digest=result['preview_digest'])
        return applied

    def refused(label, command, code, *, actor=principal):
        before = fingerprint(service)
        try:
            service.rehearse(actor, command)
        except Refusal as exc:
            assert exc.code == code, (label, exc.code)
            after = fingerprint(service)
            assert before == after, label + ': refused operation changed graph state'
            events.append({'case': label, 'outcome': 'passed', 'refusal': exc.result(), 'before': before, 'after': after}); save()
        else:
            raise AssertionError(label + ': expected refusal')

    capture = {'kind': 'capture-verification', 'id': 'VREC-P3-002', 'domain': 'lifecycle-pilot',
               'work_orders': ['WO-P3-001'], 'verifications': ['VER-P3-001'],
               'evidence': ['docs/engineering/lifecycle-pilot/evidence/WO-P3-001/assertion.json'], 'owner': 'quality-owner'}
    risk = {'kind': 'raise-risk', 'domain': 'lifecycle-pilot', 'id': 'RISK-P3-030', 'title': 'Atomic rollback fixture',
            'description': 'Neither record may survive a refused transaction.', 'action': 'Inspect both exact records and the receipt.',
            'owner': 'test-owner', 'raised_by': 'test-executor', 'threatens': ['WO-P3-001'],
            'decision_id': 'DEC-P3-030', 'recommend': 'mitigate'}
    try:
        service.readiness()
        for family, action in (('record-and-sidecar', capture), ('risk-and-decision', risk)):
            for stage in ('after_evaluation', 'after_revisions', 'after_snapshot', 'after_graph', 'before_commit'):
                value = preview(request(f'fault-{family}-{stage}', action))
                before = fingerprint(service)
                reached = []
                def fault(point, tx):
                    if point == stage:
                        reached.append(point)
                        raise RuntimeError('Deliberate qualification interruption')
                try:
                    service.rehearse(principal, value, fault=fault)
                except RuntimeError as exc:
                    assert str(exc) == 'Deliberate qualification interruption'
                else:
                    raise AssertionError('Fault did not interrupt the real transaction')
                after = fingerprint(service)
                assert reached and before == after
                with service.store.transaction() as tx:
                    assert service.store.operation(tx, principal['id'], value['operation_key']) is None
                events.append({'case': family + '-' + stage, 'outcome': 'passed', 'before': before, 'after': after}); save()

        for effect in ('unexpected-path', 'missing-sidecar'):
            original = service.evaluator.invoke
            def inject(argv, *, cwd=None):
                result = original(argv, cwd=cwd)
                if len(argv) > 3 and argv[2] == 'capture-verification' and result[0] == 0:
                    root = Path(argv[3])
                    if effect == 'unexpected-path':
                        (root/'unexpected.txt').write_text('Injected after the released command; must not commit.\n')
                    else:
                        (root/'docs/engineering/lifecycle-pilot/evidence/VREC-P3-002-evaluator.json').unlink()
                return result
            service.evaluator.invoke = inject
            try:
                refused(effect, request('refuse-' + effect, capture), 'HAG_REMOTE_UNEXPECTED_OUTPUT')
            finally:
                service.evaluator.invoke = original

        missing_test = request('missing-test-copy', capture); missing_test['test_copy'] = False
        refused('missing-test-copy', missing_test, 'HAG_REMOTE_TEST_BOUNDARY')
        refused('reader-cannot-mutate', request('reader-capture', capture), 'HAG_REMOTE_FORBIDDEN',
                actor=next(p for p in service.credentials['principals'] if p['id'] == 'reader'))
        arbitrary = request('arbitrary-command', {'kind': 'validate', 'argv': ['never-run']})
        refused('arbitrary-command', arbitrary, 'HAG_REMOTE_MALFORMED')
        wrong_schema = request('unknown-schema', capture); wrong_schema['schema'] = 'unsupported/v9'
        refused('unknown-schema', wrong_schema, 'HAG_REMOTE_MALFORMED')
        oversized = request('oversize-input', capture); oversized['padding'] = 'x' * (4 * 1024 * 1024)
        refused('oversize-input', oversized, 'HAG_REMOTE_RESOURCE_LIMIT')
        with service.evaluator.project(), service.evaluator.project():
            refused('projection-concurrency-limit', request('third-projection', capture), 'HAG_REMOTE_RESOURCE_LIMIT')
        for effect, program in (('output-bound', "print('x' * (34 * 1024 * 1024))"),
                                ('evaluator-timeout', 'import time; time.sleep(125)')):
            original = service.evaluator.invoke
            def bounded(argv, *, cwd=None):
                if len(argv) > 3 and argv[2] == 'capture-verification':
                    return original(['-c', program], cwd=cwd)
                return original(argv, cwd=cwd)
            service.evaluator.invoke = bounded
            started = time.monotonic()
            try:
                refused(effect, request(effect, capture), 'HAG_REMOTE_RESOURCE_LIMIT')
            finally:
                service.evaluator.invoke = original
            events[-1]['measured_seconds'] = round(time.monotonic() - started, 3); save()
            if effect == 'evaluator-timeout':
                assert 120 <= events[-1]['measured_seconds'] < 170

        from hosted_artifact_graph.pilot_git import encoded, decoded, SNAPSHOT
        from hosted_artifact_graph.canonical import named_digest
        export_request = {'schema':'se-harness-lifecycle-export-request/v2','test_copy':True,
            'project_id':service.project_id,'baseline_id':state['final_baseline'],
            'client':service.config['client'],'expected_evaluator':service.config['components']['evaluator']}
        selected_snapshot = service.store.selected_snapshot
        def damaged(tx, selected):
            value = copy.deepcopy(selected_snapshot(tx, selected))
            value['git_bundle'] = encoded(decoded(value['git_bundle'])[:-100])
            value.pop('snapshot_id')
            value['snapshot_id'] = 'sha256:' + named_digest(SNAPSHOT, value)
            return value
        before = fingerprint(service)
        service.store.selected_snapshot = damaged
        try:
            try:
                service.export_test(principal, export_request)
            except Refusal as exc:
                assert exc.code == 'HAG_REMOTE_BINDING_UNAVAILABLE'
                events.append({'case':'missing-Git-object-export','outcome':'passed','refusal':exc.result()}); save()
            else:
                raise AssertionError('Incomplete Git history was exported')
        finally:
            service.store.selected_snapshot = selected_snapshot
        assert before == fingerprint(service)

        contenders = []
        for number in (20, 21):
            action = {k: v for k, v in risk.items() if k not in ('decision_id', 'recommend')}
            action.update(id=f'RISK-P3-{number:03}', title='Competing test write ' + str(number))
            contenders.append(preview(request('race-' + str(number), action)))
        def attempt(value):
            try:
                return {'request': value, 'result': service.rehearse(principal, value)}
            except Refusal as exc:
                return {'request': value, 'refusal': exc.result()}
        with ThreadPoolExecutor(max_workers=2) as pool:
            outcomes = list(pool.map(attempt, contenders))
        accepted = [x for x in outcomes if 'result' in x]
        refused_values = [x for x in outcomes if 'refusal' in x]
        assert len(accepted) == len(refused_values) == 1
        assert refused_values[0]['refusal']['error']['code'] == 'HAG_REMOTE_STALE_PROJECT'
        winner = accepted[0]
        assert service.rehearse(principal, winner['request']) == winner['result']
        mutated = copy.deepcopy(winner['request']); mutated['action']['title'] += ' changed'
        refused('changed-key', mutated, 'HAG_REMOTE_KEY_REUSE')
        loser = refused_values[0]['request']
        refused('stale-project', loser, 'HAG_REMOTE_STALE_PROJECT')
        stale_preview = copy.deepcopy(loser)
        stale_preview.update(expected_project_version=winner['result']['versions']['project']['after'],
                             expected_context_version=winner['result']['view']['context_version'])
        refused('stale-preview', stale_preview, 'HAG_REMOTE_STALE_PREVIEW')
        events.append({'case': 'competing-writers-and-identical-retry', 'outcome': 'passed', 'outcomes': outcomes}); save()
        final = fingerprint(service)
        args.output.write_text(json.dumps({'state': 'store_cases_passed', 'events': events, 'final': final,
            'context': winner['result']['view'], 'last_request': winner['request'], 'last_result': winner['result'],
            'project_version': winner['result']['versions']['project']['after'],
            'remaining': ['unknown HTTP reply', 'restart and restore', 'export/replay corruption cases']}, indent=2) + '\n')
        print(json.dumps({'state': 'store_cases_passed', 'cases': len(events), 'project_version': final['project_version']}))
    finally:
        service.store.driver.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', type=Path, default=Path('/run/config/config.json'))
    parser.add_argument('--credentials', type=Path, default=Path('/run/secrets/sandbox_credentials'))
    parser.add_argument('--state', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    run(parser.parse_args())
