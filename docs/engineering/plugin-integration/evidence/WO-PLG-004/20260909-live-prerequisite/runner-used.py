"""Actual setup-skill check of an explicitly absent provided Python path."""
import argparse
from datetime import datetime, timezone
import importlib.util
import json
import os
from pathlib import Path
import shutil
import uuid

spec = importlib.util.spec_from_file_location('live_sessions', Path(__file__).with_name('live_sessions.py'))
live = importlib.util.module_from_spec(spec); spec.loader.exec_module(live)
probe, inline = live.probe, live.inline


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ['sandbox', 'claude', 'python']:
        parser.add_argument('--' + name, type=Path, required=True)
    parser.add_argument('--label', required=True)
    args = parser.parse_args()
    sandbox = args.sandbox.resolve(); profile = sandbox / 'isolated profile'
    if probe.contained(sandbox, probe.ROOT) or not profile.is_dir() or Path(args.label).name != args.label:
        parser.error('use existing external isolated profile and fresh single label')
    env = probe.child_environment(profile)
    auth = probe.execute([str(args.claude), 'auth', 'status', '--json'], sandbox, env)
    if auth['exit'] or json.loads(auth['stdout']).get('loggedIn') is not True:
        print(json.dumps({'logged_in': False})); return 2
    run = sandbox / args.label
    dest = probe.ROOT / 'docs/engineering/plugin-integration/evidence/WO-PLG-004' / args.label
    if run.exists() or dest.exists(): parser.error('fresh run/evidence label required')
    run.mkdir(); dest.mkdir()
    repo = run / 'disposable repository'; repo.mkdir()
    absent = run / 'absent provided python/python.exe'
    command = f'test -f "{absent.as_posix()}"'
    plugin = run / 'plugin with spaces'
    governance = repo / 'governance.txt'; governance.write_text('Disposable prerequisite observation; no authority granted.\n', encoding='utf-8')
    config = {'interpreter': str(run / 'absent evaluator/python.exe'), 'event_log': str(run / 'events.jsonl'),
              'governance': str(governance), 'archive': probe.ARCHIVE, 'payload': probe.PAYLOAD}
    powershell = str(Path(os.environ['SystemRoot']) / 'System32/WindowsPowerShell/v1.0/powershell.exe')
    probe.create_plugin(plugin, config, powershell)
    manifest = plugin / '.claude-plugin/plugin.json'; d=json.loads(manifest.read_text()); d['name']='verity-plane-prerequisite-probe'; probe.dump(manifest,d)
    skill = plugin / 'skills/setup/SKILL.md'
    skill.write_text('---\nname: setup\ndescription: Check the explicitly selected provided Python prerequisite.\n---\n'
        'This is an authorized disposable prerequisite observation. The provided Python path selected for this trial is '
        + absent.as_posix() + '. Run exactly this read-only Bash command, with no added syntax:\n\n`' + command + '`\n\n'
        'If the check fails, tell the operator: Python 3.11+ with venv and ensurepip must be installed or supplied before '
        'plugin setup can continue. Do not install Python, invoke another interpreter, create an environment, initialize '
        'the repository or claim readiness. This test says nothing about other Python installations. Stop after the check.\n', encoding='utf-8')
    probe.dump(plugin / 'hooks/hooks.json', {'hooks': {e: [{'hooks': [{'type':'command','shell':'powershell','command':inline.INLINE,'timeout':25}]}]
                       for e in ['SessionStart','PreToolUse']}})
    settings,mcp=run/'settings.json',run/'empty-mcp.json';probe.dump(settings,{'disableAllHooks':False});probe.dump(mcp,{'mcpServers':{}})
    normal=Path(os.environ['USERPROFILE']);watched=[normal/'.claude.json',normal/'.claude/settings.json',normal/'.claude/.credentials.json',normal/'.claude/plugins/installed_plugins.json',normal/'.claude/plugins/known_marketplaces.json']
    before=probe.metadata(watched);repo_before={p.relative_to(repo).as_posix():probe.digest(p) for p in repo.rglob('*') if p.is_file()}
    for p in plugin.rglob('*'):
        if p.is_file():
            q=dest/'fixture'/p.relative_to(plugin);q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,q)
    shutil.copyfile(__file__,dest/'runner-used.py')
    probe.publish_json(dest/'identities.json',{'at':datetime.now(timezone.utc).isoformat(),
        'host':probe.execute([str(args.claude),'--version'],repo,env),
        'actual_available_provided_python':probe.execute([str(args.python),'-I','-c','import sys,venv,ensurepip;print(sys.version);print(sys.executable);print(ensurepip.version())'],repo,env),
        'source_sha256':{p.name:probe.digest(p) for p in probe.HERE.iterdir() if p.is_file()},
        'selected_absent_python':str(absent),'selected_absent_python_exists_before':absent.exists(),
        'older_than_311':'unavailable: no such provided interpreter selected for this trial',
        'unusable_venv_ensurepip':'unavailable: actual supplied interpreter has both modules; it was not damaged or replaced',
        'documentation':probe.DOCS})
    debug=run/'host.debug.txt'
    argv=[str(args.claude),'--setting-sources','user','--settings',str(settings),'--plugin-dir',str(plugin),
          '--strict-mcp-config','--mcp-config',str(mcp),'-p','/verity-plane-prerequisite-probe:setup',
          '--tools','Bash,Skill','--permission-mode','manual','--permission-prompts','none',
          '--allowedTools','Bash('+command+')','--max-turns','3','--max-budget-usd','0.75',
          '--output-format','stream-json','--verbose','--include-hook-events','--debug-file',str(debug),'--session-id',str(uuid.uuid4())]
    result=probe.execute(argv,repo,env,timeout=120)
    if debug.exists():probe.publish_capture(debug,dest/'host.debug.txt')
    events=probe.events(Path(config['event_log']));probe.publish_capture(Path(config['event_log']),dest/'events.jsonl')
    repo_after={p.relative_to(repo).as_posix():probe.digest(p) for p in repo.rglob('*') if p.is_file()}
    probe.save_case(dest/'C02',[result],'Actual setup entry checks the deliberately absent provided Python and reports the prerequisite.',
        {'events':events,'selected_absent_python_exists_after':absent.exists(),'repository_before':repo_before,'repository_after':repo_after,
         'actual_result':live.result_message(result),'old_python':'unavailable','unusable_venv_ensurepip':'unavailable',
         'governance_readiness':False,'normal_profile_before':before,'normal_profile_after':probe.metadata(watched)},
        'unavailable',identity_evidence=(dest/'identities.json').relative_to(probe.ROOT).as_posix())
    print(json.dumps({'exit':result['exit'],'result':live.result_message(result).get('result'),
        'normal_profile_metadata_equal':before==probe.metadata(watched),'repository_unchanged':repo_before==repo_after}))
    return 0


if __name__=='__main__':raise SystemExit(main())
