"""Check the approved evidence relocation and Windows checkout path budget.

Read-only repair acceptance. Original logs/manifests describe their original
locations; the map reconciles those paths without rewriting observed payloads.
"""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath, PureWindowsPath
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--checkout-root', default='D:/a/se_harness/se_harness')
    parser.add_argument('--max-full-path', type=int, default=250)
    args = parser.parse_args()
    root = args.root.resolve()
    prefix = 'docs/engineering/plugin-integration/'
    plan_path = prefix + 'evidence/WO-PLG-017/path-plan.json'
    map_path = prefix + 'evidence/WO-PLG-011/native-path-map.json'
    sha = lambda data: hashlib.sha256(data).hexdigest()

    def git(*arguments):
        result = subprocess.run(['git', '-C', str(root), '-c', 'safe.directory=' + root.as_posix(),
                                 '-c', 'core.longpaths=true', *arguments], capture_output=True, check=True)
        return result.stdout

    def path(relative):
        if not isinstance(relative, str) or '\\' in relative or ':' in relative:
            raise ValueError('Invalid repository-relative path')
        parts = PurePosixPath(relative)
        if parts.is_absolute() or '..' in parts.parts or str(parts) != relative:
            raise ValueError('Non-canonical repository-relative path')
        resolved = (root / relative).resolve()
        if not resolved.is_relative_to(root):
            raise ValueError('Path leaves selected checkout')
        return resolved

    plan_bytes = path(plan_path).read_bytes()
    plan = json.loads(plan_bytes)
    mapping = json.loads(path(map_path).read_bytes())
    if mapping['schema'] != 'se-harness-evidence-relocation-v1' or mapping['evidence_bytes_modified'] is not False:
        raise ValueError('Unexpected relocation declaration')
    if mapping['source_plan_sha256'] != sha(plan_bytes) or mapping['source_commit'] != plan['source_commit']:
        raise ValueError('Map is not bound to the approved plan')
    git('merge-base', '--is-ancestor', mapping['source_commit'], 'HEAD')
    old_roots = [prefix + f'evidence/WO-PLG-011/acceptance/linux-replay-attempt{i}/native-products/' for i in (1, 2)]
    original_paths = set(git('ls-tree', '-r', '--name-only', mapping['source_commit'], *old_roots).decode().splitlines())
    rows = mapping['files']
    original_set = {row['original_path'] for row in rows}
    destinations = {row['retained_path'] for row in rows}
    expected = [{**row, 'retained_path': row['proposed_path']} for row in plan['files']]
    expected = [{k: v for k, v in row.items() if k != 'proposed_path'} for row in expected]
    if rows != expected or len(rows) != 55 or len(destinations) != 55 or original_set != original_paths:
        raise ValueError('Relocation count, path set or approved mapping differs')
    for row in rows:
        if not row['retained_path'].startswith(prefix + 'evidence/WO-PLG-011/native/'):
            raise ValueError('Unexpected retention destination')
        original = git('show', mapping['source_commit'] + ':' + row['original_path'])
        retained = path(row['retained_path']).read_bytes()
        if retained != original or len(retained) != row['bytes'] or sha(retained) != row['sha256']:
            raise ValueError('Changed evidence payload: ' + row['original_path'])
        if path(row['original_path']).exists():
            raise ValueError('Old long path is still present: ' + row['original_path'])
    # Staging is performed by the caller. This check never updates the Git index.
    tracked = git('ls-files', '-z').decode().rstrip('\0').split('\0')
    if original_set.intersection(tracked) or not destinations.issubset(tracked):
        raise ValueError('Index does not contain the planned relocation')
    lengths = [(len(str(PureWindowsPath(args.checkout_root) / rel)), rel) for rel in tracked]
    over_budget = [(length, rel) for length, rel in lengths if length > args.max_full_path]
    if over_budget:
        raise ValueError('Windows checkout path budget exceeded: ' + repr(over_budget))
    # Preserve the ready record and its captured evaluator facts exactly at G.
    immutable = [prefix + 'verification-records/VREC-PLG-008.md', prefix + 'evidence/VREC-PLG-008-evaluator.json']
    for rel in immutable:
        if path(rel).read_bytes() != git('show', mapping['source_commit'] + ':' + rel):
            raise ValueError('Historical verification evidence changed: ' + rel)
    print(json.dumps({'passed': True, 'mapped_files': len(rows), 'payload_bytes_unchanged': True,
                      'source_commit': mapping['source_commit'], 'preserved_vrec': 'VREC-PLG-008',
                      'max_full_path': max(length for length, _ in lengths), 'path_budget': args.max_full_path,
                      'checkout_root': args.checkout_root, 'scope': 'Retained evidence bytes and paths only; no assurance decision'}, indent=2))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, KeyError, OSError, subprocess.SubprocessError) as exc:
        print(json.dumps({'passed': False, 'error': str(exc)}), file=sys.stderr)
        raise SystemExit(1)
