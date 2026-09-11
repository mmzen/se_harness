import hashlib, json, os, pathlib, shutil, subprocess, sys, tomllib

OUT = pathlib.Path(__file__).resolve().parent
SOURCE = OUT.parent / 'se-harness-plugin-evidence-path-fix'
G = '7fe82c95823503e54d2e35e00d8c409a6dd4b065'
C = 'e9418644e22497e622b706cb228f0cd8b36f3b5b'
BASE = 'docs/engineering/plugin-integration/evidence/WO-PLG-011/'
VREC = 'docs/engineering/plugin-integration/verification-records/VREC-PLG-008.md'
ENV = dict(os.environ, GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM='1', GIT_OPTIONAL_LOCKS='0')

def sha(b): return hashlib.sha256(b).hexdigest()
def save(name, data):
    path = OUT / name
    if path.exists(): raise RuntimeError('Refusing overwrite: ' + str(path))
    path.write_bytes(data)
def js(name, value): save(name, (json.dumps(value, sort_keys=True, indent=2) + '\n').encode())
def call(name, args, inp=None, expected=0, safe=True):
    argv = ['git'] + (['-c', 'safe.directory=' + SOURCE.as_posix()] if safe else []) + ['-C', str(SOURCE)] + args
    p = subprocess.run(argv, input=inp, capture_output=True, env=ENV, timeout=60)
    save(name + '.stdout', p.stdout); save(name + '.stderr', p.stderr)
    js(name + '.json', dict(argv=argv, returncode=p.returncode, stdout_sha256=sha(p.stdout), stderr_sha256=sha(p.stderr), expected=expected))
    if p.returncode != expected: raise RuntimeError(name + ' failed')
    return p.stdout

save('freeze-source.py', pathlib.Path(__file__).read_bytes())
# Retain the original ownership-refusal setup condition, then use a per-call safe.directory.
call('o01-ownership-refusal', ['show', G + ':' + VREC], expected=128, safe=False)
plan_bytes = (SOURCE / 'docs/engineering/plugin-integration/evidence/WO-PLG-017/path-plan.json').read_bytes()
save('approved-path-plan.json', plan_bytes)
save('approved-work-order.md', (SOURCE / 'docs/engineering/plugin-integration/work-orders/WO-PLG-017.md').read_bytes())
plan = json.loads(plan_bytes)
assert plan['source_commit'] == G and plan['preserved_candidate'] == C
assert len(plan['files']) == 55
assert len({x['original_path'] for x in plan['files']}) == 55
assert len({x['proposed_path'] for x in plan['files']}) == 55
call('o02-c-ancestor', ['merge-base', '--is-ancestor', C, G])
tree_raw = call('o03-original-tree', ['ls-tree', '-r', '-z', G])
tree = {}
for entry in tree_raw.split(b'\0'):
    if not entry: continue
    meta, path = entry.split(b'\t', 1)
    mode, kind, oid = meta.decode().split()
    tree[path.decode()] = dict(mode=mode, type=kind, oid=oid)
paths = sorted(p for p in tree if p.startswith(BASE) or p == VREC or p == 'docs/engineering/plugin-integration/evidence/VREC-PLG-008-evaluator.json' or p.startswith('tests/plugin_integration/evidence-skill/'))
objects = call('o04-original-objects', ['cat-file', '--batch'], ''.join(G + ':' + p + '\n' for p in paths).encode())
cursor = 0; contents = {}; inventory = {}
for path in paths:
    end = objects.index(b'\n', cursor)
    oid, kind, size = objects[cursor:end].decode().split()
    size = int(size); data = objects[end+1:end+1+size]; cursor = end+size+2
    assert kind == 'blob' and oid == tree[path]['oid']
    contents[path] = data
    inventory[path] = dict(**tree[path], bytes=size, sha256=sha(data))
assert cursor == len(objects)
front = tomllib.loads(contents[VREC].decode().split('+++')[1])
selected = front['evidence_paths']
assert len(selected) == 95 and len(set(selected)) == 95
assert front['commit'] == C
assert sha(contents[front['evaluator_evidence_path']]) == front['evaluator_evidence_sha256']
mapped = []
for n, row in enumerate(plan['files'], 1):
    old, new = row['original_path'], row['proposed_path']
    data = contents[old]
    assert sha(data) == row['sha256'] and len(data) == row['bytes']
    assert new not in tree and old not in selected
    flat = 'p%03d.bin' % n
    save(flat, data)
    mapped.append(dict(row, retained_original=flat, git_blob=tree[old]['oid']))
save('original-vrec008.md', contents[VREC]); save('original-evaluator008.json', contents[front['evaluator_evidence_path']])
js('oracle.json', dict(schema='wo017-independent-oracle-v1', source_commit=G, preserved_candidate=C,
    governing_plan_sha256=sha(plan_bytes), mapped=mapped, original_inventory=inventory,
    selected_evidence_paths=selected, vrec_path=VREC, evaluator_path=front['evaluator_evidence_path'],
    only_allowed_original_evidence_edit=BASE+'README.md', readme_rule='Original bytes retained as prefix; appended relocation explanation only.',
    windows_test=dict(core_longpaths=False, full_path_budget=250, ci_root='D:/a/se_harness/se_harness'),
    expectations=['Exact 55 moves, byte counts and SHA256; all old paths absent and exact new set.',
      'Every other original WO011 evidence byte and retained replay test byte unchanged except README append.',
      'Original VREC008, evaluator sidecar, and 94 selected paths unchanged; README original retained at C and G.',
      'C and G remain ancestors of repair commit; fresh Windows checkout with longpaths false.',
      'Linux reconciliation/readability and replay-input presence only, not new behavior observations.',
      'One-byte payload tamper in disposable checkout must make root checker fail; restore exact original bytes.']))
save('oracle.md', b'# Independent WO-PLG-017 oracle\n\nFrozen from approved path-plan and immutable Git G, before reading the repair checker. The exact map has 55 files; the VREC selects 95 paths including the sole permitted README append. Original source evidence and retained replay inputs are hash-bound in oracle.json. Windows checkout must use core.longpaths=false. Linux is a read/reconciliation check, not a new behavioral replay. The intentionally corrupted disposable payload must be rejected. Original failure and all successful raw command records are retained without replacement.\n')
js('oracle-freeze.json', dict(oracle_sha256=sha((OUT/'oracle.json').read_bytes()), files=55, original_file_count=len(inventory), selected_paths=len(selected), source_bytes=sum(x['bytes'] for x in inventory.values()), checker_read=False))
print((OUT/'oracle-freeze.json').read_text())
