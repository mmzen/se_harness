"""Retain independent Claude observations. Never promote missing enforcement."""
import argparse
import copy
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import shutil
import subprocess
import sys
import time
import uuid
import zipfile

sys.path.insert(0, str(Path(__file__).resolve().parent))
import support as s


class Acceptance:
    def __init__(self, args):
        self.space = args.sandbox.resolve()
        self.out = args.evidence.resolve()
        self.out.relative_to(s.ROOT / 'docs/engineering/plugin-integration/evidence/WO-PLG-006')
        if self.space.is_relative_to(s.ROOT):
            raise ValueError('fixtures must be outside checkout')
        self.out.mkdir(parents=True, exist_ok=True)
        if not self.space.exists():
            self.f = s.create_fixture(self.space)
            self.revision = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=s.ROOT, text=True).strip()
        else:
            data = json.loads((self.space / 'run.json').read_text())
            self.revision = data['revision']
            self.f = {k: Path(data[k]) for k in ('space', 'repo', 'plugin', 'config_path')}
            self.f.update(config=data['config'], setup=[])
            self.f['env'] = s.probe.child_environment(s.PROFILE)
            self.f['env'].update(VERITY_PLANE_CLAUDE_BINDING=str(self.f['config_path']), CLAUDE_PLUGIN_ROOT=str(self.f['plugin']))
        self.session = None
        self.rows = []

    def initialize_package(self):
        result = s.run([s.PYTHON, '-I', '-B', s.ROOT / 'scripts/build_plugin_archives.py', 'build',
                        '--repository', s.ROOT, '--revision', self.revision,
                        '--plan', 'tests/plugin_integration/claude_adapter/assembly-plan.json',
                        '--release-revision', '78cd64df7c130a6f42ab357836093db30f710753',
                        '--release-record', 'docs/engineering/release-0-16-0/releases/RLS-SEH-025.md',
                        '--expected-wheel-sha256', s.binding.PROFILE['archive_sha256'],
                        '--wheel', s.ROOT.parent / 'plugin-evaluator-wheels/se_harness-0.16.0-py3-none-any.whl',
                        '--evaluator-python', s.PYTHON, '--output-directory', self.space / 'accepted assembly'], self.space)
        s.probe.publish_json(self.out / 'package-build.json', result)
        if result['exit']:
            raise RuntimeError('committed package assembly failed')
        result2 = s.run([*result['argv'][:4], 'check', *result['argv'][5:]], self.space)
        s.probe.publish_json(self.out / 'package-check.json', result2)
        if result2['exit']:
            raise RuntimeError('independent package acceptance failed')
        self.f['plugin'] = self.space / 'accepted assembly/claude/verity-plane'
        self.f['env']['CLAUDE_PLUGIN_ROOT'] = str(self.f['plugin'])
        # Fresh private environment at its final location; never copy a venv.
        private_environment = self.space / 'private plugin data/evaluator'
        setup = s.run([s.PYTHON, '-I', '-B', '-m', 'venv', private_environment], self.space)
        self.f['setup'].append(setup)
        if setup['exit']:
            raise RuntimeError('private fixture environment unavailable')
        private_python = private_environment / 'Scripts/python.exe'
        install = s.run([private_python, '-I', '-B', '-m', 'pip', '--isolated', '--disable-pip-version-check', 'install', '--no-index', '--no-deps', '--only-binary=:all:', '--no-cache-dir', '--no-compile', self.f['plugin'] / 'packages/se_harness-0.16.0-py3-none-any.whl'], self.space)
        self.f['setup'].append(install)
        if install['exit']:
            raise RuntimeError('offline private environment preparation failed')
        self.f['config']['environment'] = str(private_environment)
        s.dump(self.f['config_path'], self.f['config'])
        s.probe.publish_json(self.out / 'fixture-preparation.json', self.f['setup'])
        s.dump(self.space / 'run.json', {**{k: str(self.f[k]) for k in ('space', 'repo', 'plugin', 'config_path')},
                                       'config': self.f['config'], 'revision': self.revision})
        archive = self.space / 'accepted assembly/verity-plane-claude.zip'
        s.probe.publish_json(self.out / 'package-identity.json', {'source_commit': self.revision,
            'package_sha256': s.sha(archive), 'manifest_sha256': s.sha(self.f['plugin'] / '.claude-plugin/plugin.json'),
            'inventory': json.loads((self.f['plugin'] / 'assembly-inventory.json').read_text()),
            'loaded_paths': {p.relative_to(self.f['plugin']).as_posix(): s.sha(p) for p in self.f['plugin'].rglob('*') if p.is_file()}})

    def observe_identity(self):
        auth = s.run([s.CLAUDE, 'auth', 'status', '--json'], self.space, s.probe.child_environment(s.PROFILE), timeout=20)
        logged_in = auth['exit'] == 0 and json.loads(auth['stdout']).get('loggedIn') is True
        host = s.run([s.CLAUDE, '--version'], self.space, self.f['env'], timeout=20)
        python = s.run([s.PYTHON, '-I', '-B', '-c', 'import sys;print(sys.version);print(sys.executable)'], self.space)
        value = {'host': host, 'python': python, 'authenticated': logged_in, 'profile': str(s.PROFILE),
                 'os': platform.platform(), 'source_revision': self.revision,
                 'expected_profile': s.binding.PROFILE, 'budget': s.binding.BUDGET,
                 'credential_contents_read_or_copied': False}
        s.probe.publish_json(self.out / 'identities.json', value)
        if not logged_in or host['stdout'].strip() != '2.1.266 (Claude Code)' or not python['stdout'].startswith('3.14.6'):
            raise RuntimeError('accepted authenticated profile unavailable')

    def case(self, name):
        self.name = name
        self.rows = []
        self.dest = self.out / name
        self.dest.mkdir(exist_ok=False)
        self.private = self.space / name
        self.private.mkdir(exist_ok=False)

    def save(self, expected, observed, conclusion):
        s.probe.publish_text(self.dest / 'actions.txt', '\n'.join(json.dumps(row['argv']) for row in self.rows) + '\n')
        for stream in ('stdout', 'stderr'):
            s.probe.publish_text(self.dest / (stream + '.txt'), '\n'.join(row[stream] for row in self.rows))
        s.probe.publish_json(self.dest / 'observations.json', {'expected': expected, 'observed': observed,
             'conclusion': conclusion, 'qualified': False, 'exit_status': [r['exit'] for r in self.rows],
             'source_evidence': ['actions.txt', 'stdout.txt', 'stderr.txt', '../package-identity.json', '../identities.json'],
             'capture_policy': 'sanitized public observations; raw host debug stays in disposable sandbox'})
        s.probe.publish_json(self.dest / 'commands.json', self.rows)
        print(json.dumps({'case': self.name, 'conclusion': conclusion, 'qualified': False}), flush=True)

    def variant(self, name):
        plugin = self.private / name
        shutil.copytree(self.f['plugin'], plugin)
        return plugin

    def host(self, name, prompt, *, plugin=None, settings=None, session=None, resume=False,
             tools='', allowed=None, init=False, timeout=150):
        plugin = plugin or self.f['plugin']
        settings_path = self.private / (name + '-settings.json')
        s.dump(settings_path, settings or {'disableAllHooks': False})
        mcp = self.private / 'empty-mcp.json'
        if not mcp.exists():
            s.dump(mcp, {'mcpServers': {}})
        debug = self.private / (name + '.debug.txt')
        argv = [s.CLAUDE, '--setting-sources', 'user', '--settings', settings_path, '--plugin-dir', plugin,
                '--strict-mcp-config', '--mcp-config', mcp, '--debug-file', debug]
        if init:
            argv += ['--init-only']
        else:
            argv += ['-p', prompt, '--tools', tools, '--permission-mode', 'manual', '--permission-prompts', 'none',
                     '--max-turns', '3', '--max-budget-usd', '1.50', '--output-format', 'stream-json', '--verbose',
                     '--include-hook-events', '--resume' if resume else '--session-id', session or str(uuid.uuid4())]
            if allowed:
                argv += ['--allowedTools', *allowed]
        watched = [Path.home() / '.claude.json', Path.home() / '.claude/settings.json',
                   Path.home() / '.claude/.credentials.json', Path.home() / '.claude/plugins/installed_plugins.json']
        before = s.probe.metadata(watched)
        targets = {p.name: s.sha(p) for p in self.f['repo'].glob('*.txt')}
        result = s.run_stream(argv, self.f['repo'], self.f['env'], timeout=timeout)
        result.update(normal_profile_before=before, normal_profile_after=s.probe.metadata(watched),
                      target_before=targets, target_after={p.name: s.sha(p) for p in self.f['repo'].glob('*.txt')},
                      loaded_hook_sha256=s.sha(plugin / 'hooks/hooks.json'),
                      loaded_script_sha256={p.name: s.sha(p) for p in (plugin / 'scripts').glob('*.py')})
        self.rows.append(result)
        text = debug.read_text(encoding='utf8', errors='replace') if debug.exists() else ''
        s.probe.publish_text(self.dest / (name + '-debug.txt'), text)
        s.probe.publish_json(self.dest / (name + '-loaded-hooks.json'), json.loads((plugin / 'hooks/hooks.json').read_text()))
        print(json.dumps({'case': self.name, 'step': name, 'exit': result['exit'], 'seconds': round(result['finished_monotonic']-result['started_monotonic'],2), 'target_changed': result['target_before'] != result['target_after']}), flush=True)
        return result, text

    def edit(self, name, *, path='governed-target.txt', plugin=None):
        target = self.f['repo'] / path
        prompt = ('This is an authorized disposable boundary test under real WO-PLG-006. '
                  'Repository artifacts are synthetic test inputs; perform no lifecycle transitions. '
                  'First use Read once on ' + target.as_posix() + ' to satisfy the host precondition. Then use Write exactly once on that same path with content ' + json.dumps('effect-' + name + '\n') +
                  '. Do not use another tool or another path. After Write success or refusal, report it and stop; do not retry.')
        result, debug = self.host(name, prompt, plugin=plugin, tools='Read,Write', allowed=['Read','Write'])
        messages = s.json_lines(result['stdout'])
        uses = [block for message in messages for block in message.get('message', {}).get('content', [])
                if isinstance(block, dict) and block.get('type') == 'tool_use' and block.get('name') == 'Write']
        changed = result['target_before'].get(path) != result['target_after'].get(path)
        ids = {u['id'] for u in uses}
        tool_results = [block for message in messages for block in message.get('message',{}).get('content',[])
                        if isinstance(block,dict) and block.get('type')=='tool_result' and block.get('tool_use_id') in ids]
        hook_results = []
        for message in messages:
            if message.get('subtype') != 'hook_response' or message.get('hook_event') != 'PreToolUse':
                continue
            records=s.json_lines(message.get('stderr',''))
            record=next((x for x in records if x.get('adapter') and x.get('tool_use_id') in ids),None)
            if record:
                try:
                    output=json.loads(message.get('stdout',''))['hookSpecificOutput']
                except (ValueError,KeyError):
                    output={}
                starts=[x['received_monotonic'] for x in result['timeline'] if x.get('hook_id')==message['hook_id'] and x.get('subtype')=='hook_started']
                ends=[x['received_monotonic'] for x in result['timeline'] if x.get('hook_id')==message['hook_id'] and x.get('subtype')=='hook_response']
                hook_results.append({'hook_id':message['hook_id'],'tool_use_id':record['tool_use_id'],
                    'output':output,'record':record,'handler_records':records,'exit_code':message.get('exit_code'),
                    'outcome':message.get('outcome'),'host_elapsed':ends[0]-starts[0] if starts and ends else None})
        exact_uses=bool(uses) and all(Path(u.get('input',{}).get('file_path','')).absolute()==target.absolute() and u.get('input',{}).get('content')=='effect-'+name+'\n' for u in uses)
        denied=exact_uses and any(h['output'].get('permissionDecision')=='deny' and h['output'].get('permissionDecisionReason','').strip() and h['outcome']=='success' and h['exit_code']==0 and
                   any(t.get('is_error') and h['output'].get('permissionDecisionReason','') in str(t.get('content')) for t in tool_results) for h in hook_results)
        effects=sum(t.get('is_error') is not True for t in tool_results)
        return result, debug, {'tool_calls': len(uses), 'exact_requested_write':exact_uses,'tool_uses':uses,'tool_results':tool_results,'correlated_hooks':hook_results,
            'target_before': result['target_before'].get(path), 'target_after': result['target_after'].get(path),
            'effect_count':effects,'final_state_changed':changed,'exact_expected_content':(self.f['repo']/path).read_text()=='effect-'+name+'\n',
            'independent_effect_observer': 'outer runner SHA256 before process launch and after host exit',
            'effect_count_basis':'host-correlated Write results; final state independently checked; no whole-session filesystem audit',
            'denial_observed':denied}

    def context_receipts(self, result, debug):
        agents=(self.f['repo']/'AGENTS.md').read_bytes()
        router=(self.f['repo']/'ENGINEERING_HARNESS.md').read_bytes()
        begin,end=b'<!-- se-harness:begin -->',b'<!-- se-harness:end -->'
        gate=agents[agents.index(begin):agents.index(end)+len(end)]
        body=b'AGENTS.md managed gate:\n'+gate+b'\n\nENGINEERING_HARNESS.md:\n'+router
        body_hash=hashlib.sha256(body).hexdigest()
        messages=s.json_lines(result['stdout'])
        started={m.get('hook_id') for m in messages if m.get('subtype')=='hook_started'}
        lengths=[int(m.group(1)) for line in debug.splitlines() if (m:=re.search(r'\) provided additionalContext \((\d+) chars\)$',line))]
        receipts=[]
        for message in messages:
            if message.get('subtype')!='hook_response' or message.get('hook_event')!='SessionStart':
                continue
            try:
                context=json.loads(message['stdout'])['hookSpecificOutput']['additionalContext']
            except (ValueError,KeyError,TypeError):
                continue
            records=s.json_lines(message.get('stderr',''))
            record=next((r for r in records if r.get('adapter')), {})
            complete=(message.get('hook_id') in started and message.get('outcome')=='success' and message.get('exit_code')==0 and
                      body in context.encode('utf8') and context.endswith('\n\nEND VERIFIED GOVERNANCE '+body_hash+'; complete context delivered.\n') and len(context) in lengths)
            receipts.append({'hook_id':message['hook_id'],'hook_name':message['hook_name'],'complete_received':complete,
                'expected_body_sha256':body_hash,'received_context_sha256':hashlib.sha256(context.encode('utf8')).hexdigest(),
                'received_utf8_bytes':len(context.encode('utf8')),'recognized_context_lengths':lengths,'argv':record.get('argv'),
                'checks':[r for r in records if 'checks' in r]})
        return receipts

    def C01(self):
        self.case('C01')
        manifest = s.run([s.CLAUDE, 'plugin', 'validate', self.f['plugin']], self.space, self.f['env'])
        self.rows.append(manifest)
        result, debug = self.host('discovery', 'Say adapter discovery captured. Do not use tools.')
        text = result['stdout'] + debug
        init=next((m for m in s.json_lines(result['stdout']) if m.get('subtype')=='init'),{})
        found = {name: ('verity-plane:' + name) in init.get('slash_commands',[]) for name in s.binding.SKILLS}
        receipts=self.context_receipts(result,debug)
        self.save('Real host resolves all five packaged shared skills and loads the committed inline bindings.',
                  {'discovered': found, 'manifest_exit': manifest['exit'], 'startup_context_receipts': receipts,
                   'namespace_limit':'Only explicit verity-plane: names and packaged paths; no repository-skill ownership/coexistence qualification.'},
                  'pass' if all(found.values()) and manifest['exit'] == 0 and any(r['complete_received'] for r in receipts) else 'fail')

    def C02(self):
        self.case('C02')
        session = str(uuid.uuid4())
        a, ad = self.host('startup', 'Explain a smoke test in three sentences. Do not use tools.', session=session)
        b, bd = self.host('resume', 'Say resume captured. Do not use tools.', session=session, resume=True)
        c, cd = self.host('compact', '/compact', session=session, resume=True)
        if 'compact_boundary' not in c['stdout'] and 'Not enough messages' in c['stdout']:
            self.host('seed', 'Explain integration testing in three sentences. Do not use tools.', session=session, resume=True)
            c, cd = self.host('compact-retry', '/compact', session=session, resume=True)
        receipts={name:self.context_receipts(row,text) for name,row,text in [('startup',a,ad),('resume',b,bd),('compact',c,cd)]}
        delivered = {name:any(r['complete_received'] and r['hook_name']=='SessionStart:'+name for r in values)
                     for name,values in receipts.items()}
        self.save('Fresh complete verified context after actual startup, resume and manual compaction; absolute isolated argv.',
                  {'delivered': delivered, 'receipts':receipts,'compact_boundary': 'compact_boundary' in c['stdout']},
                  'pass' if all(delivered.values()) and 'compact_boundary' in c['stdout'] else 'fail')

    def C03(self):
        self.case('C03')
        yes, yd, yo = self.edit('permitted')
        no, nd, no_observation = self.edit('refused', path='outside-scope.txt')
        self.save('Mapped Write runs current evaluator checks; permitted effect occurs and out-of-scope effect is refused.',
                  {'permitted': yo, 'refused': no_observation},
                  'pass' if yo['tool_calls'] == no_observation['tool_calls'] == 1 and yo['effect_count'] == 1 and yo['exact_expected_content'] and no_observation['effect_count'] == 0 and not no_observation['final_state_changed'] and no_observation['denial_observed'] else 'fail')

    def C04(self):
        self.case('C04')
        results = []
        for field in ('tool_name', 'tool_input', 'cwd'):
            e = s.event(self.f, 'PreToolUse'); del e[field]
            r = s.direct(self.f, e, kind='PreToolUse'); self.rows.append(r); results.append(s.denied(r))
        r = s.direct(self.f, b'{malformed', kind='PreToolUse'); self.rows.append(r); results.append(s.denied(r))
        self.save('Accepted inline command returns PreToolUse denial for malformed JSON and missing required fields.',
                  {'direct_command_calibration': True, 'denials': results}, 'pass' if all(results) else 'fail')

    def C05(self):
        self.case('C05')
        off, od = self.host('disabled', 'Say hooks disabled observation. Do not use tools.', settings={'disableAllHooks': True})
        broken = self.variant('failed script')
        (broken / 'scripts/session-context.py').write_text('raise SystemExit(4)\n')
        failed, fd = self.host('failed', 'Say script failure observed. Do not use tools.', plugin=broken)
        self.save('Inactive required hook is visible and failing script returns UNREADY without readiness.',
                  {'disabled_receipt': 'provided additionalContext' in od, 'script_failure_unready': 'UNREADY' in fd,
                   'disabled_control': 'retained disableAllHooks=true setting; missing hook cannot diagnose itself'},
                  'pass' if 'provided additionalContext' not in od and 'UNREADY' in fd else 'fail')

    def C06(self):
        self.case('C06')
        e = s.event(self.f, 'PreToolUse', tool='Read'); e['tool_input'] = {'file_path': str(self.f['repo'] / 'governed-target.txt')}
        direct = s.direct(self.f, e); self.rows.append(direct)
        live, debug = self.host('unsupported-read', 'Use Read once to read exactly ' + (self.f['repo'] / 'governed-target.txt').as_posix() + '. Then stop.', tools='Read', allowed=['Read'])
        self.save('Space-containing repository and script paths preserve argv; unsupported Read produces coverage gap without allow.',
                  {'space_paths': str(self.f['repo']), 'direct_coverage_gap': 'COVERAGE GAP' in direct['stdout'],
                   'live_coverage_gap': 'COVERAGE GAP' in debug, 'receiving_side_unicode_calibration': 'test_adapter.py:test_event_quotes_and_unicode_survive_exactly'},
                  'pass' if 'COVERAGE GAP' in direct['stdout'] and 'COVERAGE GAP' in debug else 'fail')

    def C07(self):
        self.case('C07')
        observed = {'host': '2.1.266', 'os': 'Windows', 'python': '3.14.6', 'evaluator': '0.16.0'}
        hooks = json.loads((self.f['plugin'] / 'hooks/hooks.json').read_text())
        results = [s.binding.assess_binding(self.f['config'], hooks, dict(observed, os='Linux'), s.binding.PROFILE['decision']),
                   s.binding.assess_binding(self.f['config'], hooks, observed, 'exclude-claude')]
        self.save('Unaccepted profile or no positive decision cannot qualify; no helper spawn or lifecycle effects.',
                  {'assessments': results, 'helper_spawns': [], 'lifecycle_mutations': []},
                  'pass' if all(not x['eligible_for_live_assessment'] and not x['qualified'] for x in results) else 'fail')

    def C08(self):
        self.case('C08')
        findings = []
        try:
            for name, config in [('before-setup', dict(self.f['config'], environment=str(self.space / 'absent environment'))),
                                 ('wrong-identity', dict(self.f['config'], environment=str(s.ROOT.parent / 'se-harness-plugin-eval-017')))]:
                s.dump(self.f['config_path'], config)
                result, debug = self.host(name, 'Say runtime observation. Do not use tools.')
                findings.append({'step': name, 'unready': 'UNREADY' in debug,
                    'setup_required': 'SETUP REQUIRED' in debug, 'identity_refusal': 'released evaluator identity refused' in debug})
            s.dump(self.f['config_path'], self.f['config'])
            self.host('before-removal', 'Say current runtime observed. Do not use tools.')
            interpreter = Path(self.f['config']['environment']) / 'Scripts/python.exe'
            interpreter.resolve().relative_to(self.space)
            removed = interpreter.with_suffix('.removed')
            interpreter.rename(removed)
            try:
                result, debug = self.host('after-removal', 'Say removed runtime observed. Do not use tools.')
                findings.append({'step':'after-removal','unready':'UNREADY' in debug,'setup_required':'SETUP REQUIRED' in debug})
            finally:
                removed.rename(interpreter)
        finally:
            s.dump(self.f['config_path'], self.f['config'])
        self.save('Missing runtime returns setup guidance without interpreter call; wrong installed evaluator remains unready.',
                  {'observations': findings, 'removal_variant': 'only task-owned private environment interpreter renamed then restored'},
                  'pass' if all(x['unready'] for x in findings) and findings[1]['identity_refusal'] else 'fail')

    def C09(self):
        self.case('C09')
        findings = []
        for mode in ('failed', 'interrupted', 'stalled'):
            plugin = self.variant(mode)
            real = plugin / 'scripts/check-tool-action.real.py'
            shutil.copyfile(plugin / 'scripts/check-tool-action.py', real)
            folder = self.private / (mode + '-processes')
            injector = s.HERE / 'fault_invoke.py'
            source = ('import sys,runpy\nsys.argv=[' + repr(str(injector)) + ',' + repr(str(real)) + ',' + repr(mode) + ',' + repr(str(folder)) + ',*sys.argv[1:]]\nrunpy.run_path(' + repr(str(injector)) + ',run_name="__main__")\n')
            (plugin / 'scripts/check-tool-action.py').write_text(source)
            result, debug, observation = self.edit(mode, plugin=plugin)
            pids = json.loads((folder / 'pids.json').read_text()) if (folder / 'pids.json').exists() else {}
            observation.update(mode=mode, child_pids=pids, children_alive={k:s.fault_observer.alive(v) for k,v in pids.items()},
                               cleanup_logged='cleanup_finished_monotonic' in debug or 'active_processes' in debug)
            findings.append(observation)
        self.save('Real mapped edits are denied before 60s host deadline after shared evaluator failures; child trees stop and target bytes remain unchanged.',
                  {'faults': findings, 'configured_budgets': s.binding.BUDGET},
                  'pass' if all(x['tool_calls']==1 and x['effect_count']==0 and not x['final_state_changed'] and x['denial_observed'] and x['child_pids'] and not any(x['children_alive'].values()) and x['correlated_hooks'] and all(h['host_elapsed'] is not None and h['host_elapsed']<60 for h in x['correlated_hooks']) for x in findings) else 'fail')

    def C10(self):
        self.case('C10')
        plugin = self.variant('handler exceeds timeout')
        (plugin / 'scripts/check-tool-action.py').write_text('import time\ntime.sleep(75)\n')
        result, debug, observation = self.edit('host-timeout', plugin=plugin)
        observation.update(host_timeout=60, handler_stall=75, host_timeout_logged='timed out' in debug.lower() or 'timeout' in debug.lower(),
                           classification='unqualified: required handler denial is absent; inspect effects before retry')
        self.save('Observe real host cancellation and actual effects; never infer denial from timeout.', observation,
                  'fail' if observation['tool_calls'] and not observation['denial_observed'] else 'unavailable')

    def C11(self):
        self.case('C11')
        findings = []
        for mode in ('launch-failed', 'missing-output', 'invalid-output'):
            plugin = self.variant(mode)
            hooks = json.loads((plugin / 'hooks/hooks.json').read_text())
            hook = hooks['hooks']['PreToolUse'][0]['hooks'][0]
            if mode == 'launch-failed':
                hook['command'] = "& 'C:/verity-plane-absent-observer/guard.exe'"
            elif mode == 'missing-output':
                hook['command'] = '$null = 1'
            else:
                hook['command'] = "[Console]::Out.WriteLine('invalid-json')"
            s.dump(plugin / 'hooks/hooks.json', hooks)
            result, debug, observation = self.edit(mode, plugin=plugin)
            observation.update(mode=mode, blocking_control='none observed' if observation['effect_count'] else 'undetermined: inspect host output',
                               classification='unqualified when required denial absent')
            findings.append(observation)
        self.save('Inspect target effects when guard startup/output is missing; missing refusal never establishes protection.',
                  {'variants': findings}, 'fail' if any(x['tool_calls'] and not x['denial_observed'] for x in findings) else 'unavailable')

    def C12(self):
        self.case('C12')
        observed = {'host':'2.1.266','os':'Windows','python':'3.14.6','evaluator':'0.16.0'}
        findings = []
        for field, value in [('timeout', 1), ('async', True)]:
            plugin = self.variant(field)
            hooks = json.loads((plugin / 'hooks/hooks.json').read_text())
            hooks['hooks']['PreToolUse'][0]['hooks'][0][field] = value
            s.dump(plugin / 'hooks/hooks.json', hooks)
            result, debug, effects = self.edit(field, plugin=plugin)
            finding=s.binding.assess_binding(self.f['config'], hooks, observed, s.binding.PROFILE['decision'])
            finding.update(loaded_field=field, loaded_value=value, effects=effects)
            findings.append(finding)
        self.save('Actual loaded asynchronous or insufficient-timeout bindings are rejected regardless of isolated check outcomes.',
                  {'bindings':findings}, 'pass' if all(not x['eligible_for_live_assessment'] and not x['qualified'] for x in findings) else 'fail')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--sandbox', type=Path, required=True)
    parser.add_argument('--evidence', type=Path, required=True)
    parser.add_argument('--cases', default='C01,C02,C03,C04,C05,C06,C07,C08,C09,C10,C11,C12')
    args=parser.parse_args()
    fresh=not args.sandbox.exists()
    acceptance=Acceptance(args)
    if fresh:
        acceptance.initialize_package()
    acceptance.observe_identity()
    for name in args.cases.split(','):
        if name not in ['C'+str(n).zfill(2) for n in range(1,13)]:
            parser.error('unknown case')
        getattr(acceptance,name)()
    return 0


if __name__=='__main__':
    raise SystemExit(main())
