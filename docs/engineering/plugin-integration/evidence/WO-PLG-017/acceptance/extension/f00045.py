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

# Exact proposal approved for WO-PLG-017, retained at ed19676fd2af8b9754f74cbc6bc8664a92d2f803.
APPROVED_PLAN_SHA256 = '37031560322c962987513e8950b37503a642c6e474cc2a031822870467659aa9'
APPROVED_EXTENSION_SHA256 = '1927a7d61c7d6357e61047f427c0d2f1fb8e456d32dd1698efc01c7bba6f9538'


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
    if sha(plan_bytes) != APPROVED_PLAN_SHA256:
        raise ValueError('Relocation plan differs from the approved WO-PLG-017 plan')
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
    extension_bytes = path(prefix + 'evidence/WO-PLG-017/scope-extension-plan.json').read_bytes()
    if sha(extension_bytes) != APPROVED_EXTENSION_SHA256:
        raise ValueError('Supplemental plan differs from the approved scope extension')
    extension = json.loads(extension_bytes)
    supplemental = json.loads(path(extension['retention_map_destination']).read_bytes())
    if (supplemental['schema'] != 'se-harness-evidence-relocation-v1'
            or supplemental['evidence_bytes_modified'] is not False
            or supplemental['source_plan_sha256'] != APPROVED_EXTENSION_SHA256
            or supplemental['source_commit'] != extension['source_commit']):
        raise ValueError('Supplemental map is not bound to the approved extension')
    expected_extra = [{('retained_path' if key == 'proposed_path' else key): value
                       for key, value in row.items()} for row in extension['files']]
    if supplemental['files'] != expected_extra or len(expected_extra) != 1:
        raise ValueError('Supplemental mapping differs from the approved one-file extension')
    git('merge-base', '--is-ancestor', extension['source_commit'], 'HEAD')
    if path(map_path).read_bytes() != git('show', extension['source_commit'] + ':' + map_path):
        raise ValueError('Original 55-file map changed')
    extra = expected_extra[0]
    original = git('show', extension['source_commit'] + ':' + extra['original_path'])
    retained = path(extra['retained_path']).read_bytes()
    if retained != original or len(retained) != extra['bytes'] or sha(retained) != extra['sha256']:
        raise ValueError('Changed supplemental evidence payload')
    if path(extra['original_path']).exists():
        raise ValueError('Supplemental old path is still present')
    original_set.add(extra['original_path'])
    destinations.add(extra['retained_path'])
    if len(original_set) != 56 or len(destinations) != 56:
        raise ValueError('Combined relocation paths are not unique')
    # Staging is performed by the caller. This check never updates the Git index.
    tracked = git('ls-files', '-z').decode().rstrip('\0').split('\0')
    if original_set.intersection(tracked) or not destinations.issubset(tracked):
        raise ValueError('Index does not contain the planned relocation')
    lengths = [(len(str(PureWindowsPath(args.checkout_root) / rel)), rel) for rel in tracked]
    over_budget = [(length, rel) for length, rel in lengths if length > args.max_full_path]
    if over_budget:
        raise ValueError('Windows checkout path budget exceeded: ' + repr(over_budget))
    staging = extension['staging_profile']
    staging_lengths = [(len(str(PureWindowsPath(staging['root']) / rel)), rel) for rel in tracked]
    staging_excess = [(length, rel) for length, rel in staging_lengths if length > staging['maximum_full_path']]
    if staging_excess:
        raise ValueError('Windows rehearsal staging path budget exceeded: ' + repr(staging_excess))
    # Preserve the ready record and its captured evaluator facts exactly at G.
    immutable = [prefix + 'verification-records/VREC-PLG-008.md', prefix + 'evidence/VREC-PLG-008-evaluator.json']
    for rel in immutable:
        if path(rel).read_bytes() != git('show', mapping['source_commit'] + ':' + rel):
            raise ValueError('Historical verification evidence changed: ' + rel)
    print(json.dumps({'passed': True, 'mapped_files': len(destinations), 'original_map_files': len(rows),
                      'supplemental_files': len(expected_extra), 'payload_bytes_unchanged': True,
                      'source_commit': mapping['source_commit'], 'preserved_vrec': 'VREC-PLG-008',
                      'max_full_path': max(length for length, _ in lengths), 'path_budget': args.max_full_path,
                      'checkout_root': args.checkout_root,
                      'staging_root': staging['root'], 'staging_max_full_path': max(length for length, _ in staging_lengths),
                      'staging_budget': staging['maximum_full_path'],
                      'staging_limit': 'Derived profile; actual export/staging and hosted rehearsal must also pass.',
                      'scope': 'Retained evidence bytes and paths only; no assurance decision'}, indent=2))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, KeyError, OSError, subprocess.SubprocessError) as exc:
        print(json.dumps({'passed': False, 'error': str(exc)}), file=sys.stderr)
        raise SystemExit(1)
