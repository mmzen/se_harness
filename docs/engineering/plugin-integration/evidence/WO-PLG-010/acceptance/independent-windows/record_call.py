"""Transparent local call recorder, not an authority or workflow implementation."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import time

def snapshot(root):
    return {p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(root.rglob('*')) if p.is_file() and '.git' not in p.parts}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--python', required=True)
    ap.add_argument('--repo', type=Path, required=True)
    ap.add_argument('--evidence', type=Path, required=True)
    ap.add_argument('--label', required=True)
    ap.add_argument('--native', action='store_true')
    ap.add_argument('--suppress-receipt', action='store_true')
    ap.add_argument('argv', nargs=argparse.REMAINDER)
    ns = ap.parse_args()
    args = ns.argv[1:] if ns.argv[:1] == ['--'] else ns.argv
    args = [str(ns.repo.resolve()) if x == '{repo}' else x for x in args]
    command = args if ns.native else [ns.python, '-I', '-B', '-m', 'se_harness', *args]
    env = os.environ.copy()
    env.pop('PYTHONPATH', None)
    env['PATH'] = str(Path(ns.python).parent) + os.pathsep + env.get('PATH', '')
    ns.evidence.mkdir(parents=True, exist_ok=True)
    dest = ns.evidence / (ns.label+'.json')
    if dest.exists():
        raise FileExistsError(dest)
    before, started = snapshot(ns.repo), time.time()
    run = subprocess.run(command, cwd=Path(__file__).resolve().parent, env=env,
                         capture_output=True, timeout=60)
    after = snapshot(ns.repo)
    row = {'argv': command, 'cwd': str(Path(__file__).resolve().parent),
           'started_unix': started, 'duration_seconds': time.time()-started,
           'exit_code': run.returncode, 'stdout': run.stdout.decode('utf8', 'replace'),
           'stderr': run.stderr.decode('utf8', 'replace'), 'before': before, 'after': after,
           'changed_paths': [p for p in sorted(before.keys()|after.keys()) if before.get(p)!=after.get(p)]}
    dest.write_text(json.dumps(row, indent=2)+'\n', encoding='utf8')
    if ns.suppress_receipt:
        print(json.dumps({'fault_injection':'Tool receipt interrupted after process exit. Inspect current files before retry; actual process result retained for the observer.', 'record':str(dest)}))
        return
    print(json.dumps({'record': str(dest), 'exit_code': run.returncode,
                      'changed_paths': row['changed_paths']}))
    try:
        result = json.loads(row['stdout'])
        print(json.dumps({k: result.get(k) for k in ('schema', 'operation', 'state', 'findings', 'restitution', 'context', 'outcome', 'changes') if k in result}, indent=2))
    except ValueError:
        print(row['stdout'])
    if row['stderr']:
        print(row['stderr'])

if __name__ == '__main__':
    main()
