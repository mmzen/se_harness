"""Independent fixed-oracle WO017 checkout and retention verification."""
import argparse, hashlib, json, os, pathlib, platform, shutil, subprocess, sys, tempfile, time, traceback

def sha(data): return hashlib.sha256(data).hexdigest()
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--source', type=pathlib.Path, required=True)
    ap.add_argument('--oracle-root', type=pathlib.Path, required=True)
    ap.add_argument('--output', type=pathlib.Path, required=True)
    ap.add_argument('--commit', required=True)
    ap.add_argument('--branch', default='work/plugin-evidence-path-repair')
    ap.add_argument('--tamper', action='store_true')
    ap.add_argument('--plan-tamper', action='store_true')
    a = ap.parse_args()
    out = a.output.resolve(); out.mkdir(parents=True, exist_ok=False)
    source = a.source.resolve(); oracle_root = a.oracle_root.resolve()
    (out/'runner-source.py').write_bytes(pathlib.Path(__file__).read_bytes())
    oracle_bytes = (oracle_root/'oracle.json').read_bytes()
    assert sha(oracle_bytes) == '51370c2582f8360b2bc5530b677c3f41b181a8d8f3d44c99e44e166ae29cc378'
    oracle = json.loads(oracle_bytes)
    home = out/'isolated-home'; home.mkdir()
    hooks = home/'hooks'; hooks.mkdir()
    env = dict(os.environ, HOME=str(home), USERPROFILE=str(home), XDG_CONFIG_HOME=str(home),
        GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM='1', GIT_OPTIONAL_LOCKS='0',
        GIT_TERMINAL_PROMPT='0', GIT_ALLOW_PROTOCOL='file')
    # Explicit temporary Windows checkout fits the fixed 250-character budget.
    # Linux uses an independently cloned persistent disposable repository.
    if os.name == 'nt':
        temp = pathlib.Path(tempfile.gettempdir()).resolve()
        repo = pathlib.Path(tempfile.mkdtemp(prefix='p17-', dir=temp)).resolve()/'r'
        assert repo.is_relative_to(temp)
    else:
        repo = out/'repo'
    def write(name, data):
        p = out/name
        if p.exists(): raise RuntimeError('Refusing overwrite: '+str(p))
        p.write_bytes(data)
    def js(name, data): write(name, (json.dumps(data, sort_keys=True, indent=2)+'\n').encode())
    calls = []
    safe_paths = [source.as_posix(), repo.as_posix()]
    def call(label, argv, expected=0, timeout=180):
        start = time.time(); stdout = stderr = b''; code = None; error = None
        try:
            p = subprocess.run([os.fspath(x) for x in argv], capture_output=True, env=env, timeout=timeout)
            stdout, stderr, code = p.stdout, p.stderr, p.returncode
        except subprocess.TimeoutExpired as e:
            stdout, stderr = e.stdout or b'', e.stderr or b''; error = {'type':'TimeoutExpired', 'message':str(e)}
        except OSError as e:
            error = {'type':type(e).__name__, 'message':str(e)}
        write(label+'.stdout', stdout); write(label+'.stderr', stderr)
        record = dict(argv=[os.fspath(x) for x in argv], cwd=os.getcwd(), returncode=code, expected=expected,
            elapsed_seconds=time.time()-start, error=error, stdout_sha256=sha(stdout), stderr_sha256=sha(stderr))
        js(label+'.json', record); calls.append(label)
        if error or code != expected: raise RuntimeError(label+' unexpected result')
        return stdout
    def git(label, *args, target=None, expected=0):
        target = target or repo
        safe_args = [arg for p in safe_paths for arg in ('-c', 'safe.directory='+p)]
        return call(label, ['git', *safe_args,
            '-c', 'core.longpaths=false', '-c', 'core.autocrlf=false', '-c', 'core.hooksPath='+str(hooks),
            '-C', str(target), *args], expected=expected)
    def snapshot(label):
        files = {}
        for p in sorted(repo.rglob('*')):
            if p.is_file():
                rel = p.relative_to(repo).as_posix(); data = p.read_bytes()
                files[rel] = {'bytes':len(data), 'sha256':sha(data)}
        js(label+'.json', files)
        return files
    result = dict(schema='wo017-independent-checkout-v1', platform=platform.platform(), python=sys.version,
        executable=sys.executable, source=str(source), checkout=str(repo), commit=a.commit,
        oracle_sha256=sha(oracle_bytes), runner_sha256=sha(pathlib.Path(__file__).read_bytes()), passed=False)
    try:
        call('01-git-version', ['git', '--version'])
        git('02-commit-type', 'cat-file', '-t', a.commit, target=source)
        source_git_dir = git('02b-source-gitdir', 'rev-parse', '--absolute-git-dir', target=source).decode().strip()
        source_common_dir = git('02c-source-common', 'rev-parse', '--path-format=absolute', '--git-common-dir', target=source).decode().strip()
        safe_paths += [pathlib.Path(source_git_dir).as_posix(), pathlib.Path(source_common_dir).as_posix()]
        # Local upload-pack does not preserve caller command-scope trust entries.
        # Its sole global config is this disposable, exact-path test config.
        env['GIT_CONFIG_GLOBAL'] = str(home/'gitconfig')
        for n, trusted_path in enumerate(safe_paths):
            git('02d-trust-'+str(n), 'config', '--file', str(home/'gitconfig'), '--add', 'safe.directory', trusted_path, target=source)
        git('03-clone', 'clone', '--no-checkout', '--no-hardlinks', '--no-tags', '--single-branch', '--branch', a.branch, str(source), str(repo), target=source)
        git('04-longpaths-config', 'config', '--local', 'core.longpaths', 'false')
        git('05-autocrlf-config', 'config', '--local', 'core.autocrlf', 'false')
        git('06-checkout', 'checkout', '--detach', a.commit)
        assert git('07-longpaths-readback', 'config', '--local', '--get', 'core.longpaths').strip() == b'false'
        assert git('08-head', 'rev-parse', 'HEAD').decode().strip() == a.commit
        git('09-g-ancestor', 'merge-base', '--is-ancestor', oracle['source_commit'], a.commit)
        git('10-c-ancestor', 'merge-base', '--is-ancestor', oracle['preserved_candidate'], a.commit)
        tracked = git('11-tracked', 'ls-files', '-z').decode().rstrip('\0').split('\0')
        assert not git('12-clean-before', 'status', '--porcelain=v1', '--untracked-files=all')
        tracked_set = set(tracked)
        original = oracle['original_inventory']; moves = oracle['mapped']
        old = {r['original_path'] for r in moves}; new = {r['proposed_path'] for r in moves}
        base = 'docs/engineering/plugin-integration/evidence/WO-PLG-011/'
        assert len(moves) == 55 and not old.intersection(tracked_set)
        expected_evidence = ({p for p in original if p.startswith(base)} - old) | new | {base+'native-path-map.json'}
        assert {p for p in tracked_set if p.startswith(base)} == expected_evidence
        mapping_bytes = (repo/(base+'native-path-map.json')).read_bytes()
        write('relocation-map.json', mapping_bytes)
        mapping = json.loads(mapping_bytes)
        expected_rows = [{k: r[k] for k in ('original_path','sha256','bytes')} | {'retained_path':r['proposed_path']} for r in moves]
        assert mapping['files'] == expected_rows and mapping['source_commit'] == oracle['source_commit']
        assert mapping['source_plan_sha256'] == oracle['governing_plan_sha256']
        assert sha((repo/'docs/engineering/plugin-integration/evidence/WO-PLG-017/path-plan.json').read_bytes()) == oracle['governing_plan_sha256']
        relocated = []
        for row in moves:
            data = (repo/row['proposed_path']).read_bytes()
            assert data == (oracle_root/row['retained_original']).read_bytes()
            assert len(data) == row['bytes'] and sha(data) == row['sha256']
            assert not (repo/row['original_path']).exists()
            if row['proposed_path'].endswith('.json'): json.loads(data)
            else: data.decode('utf-8')
            relocated.append(dict(path=row['proposed_path'], bytes=len(data), sha256=sha(data)))
        unchanged = []; readme = oracle['only_allowed_original_evidence_edit']
        for path, info in original.items():
            if path in old or path == readme: continue
            data = (repo/path).read_bytes()
            assert len(data) == info['bytes'] and sha(data) == info['sha256'], path
            unchanged.append(path)
        readme_bytes = (repo/readme).read_bytes(); readme_original = original[readme]
        assert sha(readme_bytes[:readme_original['bytes']]) == readme_original['sha256']
        write('readme-append.txt', readme_bytes[readme_original['bytes']:])
        selected = oracle['selected_evidence_paths']
        assert len(selected) == 95 and len([p for p in selected if p in unchanged]) == 94
        lengths = [(len(str(pathlib.PureWindowsPath(repo) / p)), p) for p in tracked]
        ci_lengths = [(len(str(pathlib.PureWindowsPath('D:/a/se_harness/se_harness') / p)), p) for p in tracked]
        if os.name == 'nt': assert max(x[0] for x in lengths) <= 250
        assert max(x[0] for x in ci_lengths) <= 250
        before = snapshot('13-before-checker')
        checker = repo/'tests/plugin_integration/evidence-skill/check_retention_paths.py'
        write('checker-source.py', checker.read_bytes())
        checker_argv = [sys.executable, '-I', '-B', str(checker), '--root', str(repo), '--checkout-root', str(repo) if os.name == 'nt' else 'D:/a/se_harness/se_harness']
        checker_result = json.loads(call('14-checker-positive', checker_argv))
        assert checker_result['passed'] is True and checker_result['mapped_files'] == 55
        after = snapshot('15-after-checker')
        assert before == after, 'Read-only checker changed checkout bytes'
        if a.tamper:
            row = moves[0]; payload = repo/row['proposed_path']; original_bytes = payload.read_bytes()
            corrupted = bytes([original_bytes[0] ^ 1]) + original_bytes[1:]
            assert sum(a != b for a,b in zip(corrupted, original_bytes)) == 1
            payload.write_bytes(corrupted)
            js('16-tamper-input.json', dict(path=row['proposed_path'], byte_offset=0, original_sha256=sha(original_bytes), corrupted_sha256=sha(corrupted), bytes=len(corrupted), intentional_disposable_only=True))
            try:
                call('17-checker-reject', checker_argv, expected=1)
                rejection = json.loads((out/'17-checker-reject.stderr').read_bytes())
                assert rejection['passed'] is False and 'Changed evidence payload' in rejection['error']
                during = snapshot('18-during-tamper')
                differences = sorted(p for p in set(before) | set(during) if before.get(p) != during.get(p))
                assert differences == [row['proposed_path']], differences
            finally:
                payload.write_bytes(original_bytes)
            call('19-checker-restored', checker_argv)
            assert snapshot('20-after-restore') == before
        if a.plan_tamper:
            plan_path = repo/'docs/engineering/plugin-integration/evidence/WO-PLG-017/path-plan.json'
            map_path = repo/(base+'native-path-map.json')
            plan_original = plan_path.read_bytes(); map_original = map_path.read_bytes()
            altered_plan = json.loads(plan_original)
            altered_plan['preserved_candidate'] = '0'*40
            altered_plan_bytes = (json.dumps(altered_plan, indent=2)+'\n').encode()
            altered_map = json.loads(map_original)
            altered_map['source_plan_sha256'] = sha(altered_plan_bytes)
            altered_map_bytes = (json.dumps(altered_map, indent=2)+'\n').encode()
            js('22-plan-tamper-input.json', dict(intentional_disposable_only=True,
                changed_plan_field='preserved_candidate', changed_map_field='source_plan_sha256',
                original_plan_sha256=sha(plan_original), altered_plan_sha256=sha(altered_plan_bytes),
                original_map_sha256=sha(map_original), altered_map_sha256=sha(altered_map_bytes),
                unchanged_payloads=True))
            plan_path.write_bytes(altered_plan_bytes); map_path.write_bytes(altered_map_bytes)
            try:
                call('23-checker-plan-reject', checker_argv, expected=1)
                rejected = json.loads((out/'23-checker-plan-reject.stderr').read_bytes())
                assert rejected['passed'] is False and 'plan' in rejected['error'].lower()
                during_plan = snapshot('24-during-plan-tamper')
                differences = sorted(p for p in set(before) | set(during_plan) if before.get(p) != during_plan.get(p))
                assert differences == sorted([plan_path.relative_to(repo).as_posix(), map_path.relative_to(repo).as_posix()])
            finally:
                plan_path.write_bytes(plan_original); map_path.write_bytes(map_original)
            call('25-checker-plan-restored', checker_argv)
            assert snapshot('26-after-plan-restore') == before
        assert not git('21-clean-after', 'status', '--porcelain=v1', '--untracked-files=all')
        js('reconciliation.json', dict(relocated=relocated, unchanged_original_paths=unchanged,
            selected_unchanged_paths=[p for p in selected if p != readme], readme_append_bytes=len(readme_bytes)-readme_original['bytes'],
            retained_replay_input_paths=[p for p in unchanged if p.startswith('tests/plugin_integration/evidence-skill/') or '/acceptance/linux-replay-' in p],
            retained_original_manifest_paths=[p for p in unchanged if 'manifest' in p or 'inventory' in p],
            readability='All 55 relocated files decoded as UTF-8; JSON files parsed; no evaluator/skill behavior replay.'))
        result.update(passed=True, mapped_files=55, unchanged_original_files=len(unchanged), selected_unchanged_files=94,
            readme_original_prefix_preserved=True, tracked_files=len(tracked), max_relative_path=max(map(len,tracked)),
            actual_root_max_windows_full_path=max(lengths), ci_root_max_windows_full_path=max(ci_lengths),
            tamper_rejected=a.tamper, checkout_core_longpaths=False, checker_sha256=sha(checker.read_bytes()),
            coordinated_plan_map_tamper_rejected=a.plan_tamper,
            checker_internally_uses_longpaths_true_for_readonly_git=True, all_checkout_bytes_unchanged_after_check=True)
    except BaseException as e:
        result['error'] = {'type':type(e).__name__, 'message':str(e), 'traceback':traceback.format_exc()}
        raise
    finally:
        result['calls'] = calls
        js('result.json', result)
        print(json.dumps(result, indent=2))

if __name__ == '__main__': main()
