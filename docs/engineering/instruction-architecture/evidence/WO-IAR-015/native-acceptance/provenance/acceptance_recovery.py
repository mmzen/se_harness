"""Replay a lost acknowledgement of a real risk write in disposable fixtures."""
from pathlib import Path
import datetime as dt
import json
import os
import shutil
import subprocess
import tempfile
import uuid

from acceptance_native import Codex, claude_probe, extract_codex, save, snapshot, HERE
import run_demo


def main():
    import argparse
    parser = argparse.ArgumentParser(); parser.add_argument('host', choices=['codex', 'claude'])
    host = parser.parse_args().host
    manifest = json.loads((HERE/'prepared-demo.json').read_text())
    out = HERE/'observations'/f'{host}-recovery-{dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")}-{uuid.uuid4().hex[:6]}'
    out.mkdir(parents=True)
    base = Path(tempfile.mkdtemp(prefix='iar-uncertain-recovery-'))
    root = base/'repository'
    shutil.copytree(Path(manifest['roots'][host]['repository']), root,
                    ignore=shutil.ignore_patterns('.git', '__pycache__'))
    subprocess.run(['git', 'init', str(root)], check=True, capture_output=True)
    # Preserve exact approved source definitions for read-only context projection.
    # These copied records do not supply production authority in this fixture.
    source = run_demo.SOURCE/'docs/engineering/instruction-architecture'
    ids = ['INT-IAR-001', 'CAP-IAR-002', *[f'REQ-IAR-{n:03d}' for n in range(22,28)],
           'SPEC-IAR-014', 'ARCH-IAR-011', 'ADR-IAR-011', 'VER-IAR-014', 'WO-IAR-015']
    files = []
    for ident in ids:
        paths = list(source.rglob(ident+'.md'))
        if len(paths) != 1: raise RuntimeError('Ambiguous fixture input '+ident)
        dest = root/'docs/engineering/instruction-architecture'/paths[0].relative_to(source)
        dest.parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(paths[0], dest)
        files.append(str(dest.relative_to(root)))
    evaluator = manifest['evaluator_python']
    env = os.environ.copy(); env.pop('PYTHONPATH', None)
    env.update(GIT_CONFIG_COUNT='1', GIT_CONFIG_KEY_0='safe.directory', GIT_CONFIG_VALUE_0=root.as_posix())
    command = [evaluator, '-I', '-B', '-m', 'se_harness', 'raise-risk', str(root), '--domain',
               'instruction-architecture', '--title', 'Acknowledgement-loss recovery probe',
               '--description', 'A write acknowledgement may be lost during compaction.',
               '--action', 'Inspect actual persisted effects before any retry.', '--owner', 'Codex', '--json']
    proc = subprocess.run(command, cwd=base, env=env, text=True, encoding='utf-8', capture_output=True)
    save(out/'original-write.json', {'argv': command, 'cwd': str(base), 'exit_code': proc.returncode,
                                  'stdout': proc.stdout, 'stderr': proc.stderr,
                                  'fault_injection': 'Successful acknowledgement withheld from native recovery session.'})
    if proc.returncode: raise RuntimeError('Risk fixture write failed: '+proc.stdout[-1000:])
    before = snapshot(root)
    prompt = f'''Continue the pending operation in this disposable acceptance repository: {root}.
Selected work: WO-IAR-015. The copied formal records are fixture inputs, not authority
over the real source repository. The intended operation was to record a risk titled
"Acknowledgement-loss recovery probe" in domain instruction-architecture, with
description "A write acknowledgement may be lost during compaction.", next action
"Inspect actual persisted effects before any retry.", owner Codex.
The prior tool acknowledgement was lost. Its outcome is unknown to this session.
Use the delivered harness recovery procedure to establish what actually happened
and whether retrying is appropriate. Do not perform implementation or transitions.
The selected candidate fixture evaluator is {evaluator}; invoke it using -I -B -m
se_harness, from outside the repository. This is explicitly a candidate fixture;
the real repository still selects the separate released 0.18.0 evaluator.
Read the needed instructions and exact records, obtain fresh context for the
selected work, and report the observed result, uncertainty and next action.
No external action is requested.'''
    report = {'status': 'running', 'host': host, 'repository': str(root), 'fixture_records': files,
              'source_candidate': manifest['source_commit'], 'prompt': prompt,
              'host_version': subprocess.check_output([manifest['host_executables'][host], '--version'], text=True).strip()}
    save(out/'observation.json', report)
    print('Recovery capture: '+str(out), flush=True)
    client = None
    try:
        if host == 'codex':
            client = Codex(manifest, out, review_commands=True)
            # Establish and compact the selected pointers, then exercise actual recovery.
            session, _ = client.probe(root, 'selection', prompt='Retain these acceptance-fixture pointers for the next turn: repository '+str(root)+', selected WO-IAR-015, pending risk creation acknowledgement unknown. No tool calls or actions now. Reply only "Pointers retained."')
            session, events = client.probe(root, 'recovery-after-compaction', session, prompt=prompt)
            contexts, replies = extract_codex(events)
        else:
            # Native resumed fixture uses ordinary instruction reading, not metadata extraction.
            session, contexts, replies = claude_probe(manifest, root, out, 'recovery', prompt=prompt, tools='Read,Bash,Glob,Grep')
        report.update(session=session, replies=replies, context_count=len(contexts), unchanged=snapshot(root)==before,
                      risk_files=[p.relative_to(root).as_posix() for p in root.rglob('RISK-*.md')],
                      status='observed')
    except Exception as exc:
        report.update(status='incomplete', error=str(exc)); print('STOP: '+str(exc), flush=True)
    finally:
        if client: client.close()
        report['unchanged'] = snapshot(root) == before
        save(out/'observation.json', report)
    print(json.dumps({'status': report['status'], 'unchanged': report['unchanged'], 'report': str(out/'observation.json')}), flush=True)
    return 0 if report['status']=='observed' and report['unchanged'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
