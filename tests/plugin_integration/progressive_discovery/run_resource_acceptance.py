"""Installed-wheel adapter qualification in disposable checkouts, not native host proof."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from repository_tools.plugin_distribution import develop


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--wheel', type=Path, required=True)
    parser.add_argument('--expected-identity', type=Path, required=True)
    parser.add_argument('--legacy-wheel', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    output=args.output.resolve(); output.mkdir(parents=True,exist_ok=False)
    wheel=args.wheel.resolve(strict=True); legacy=args.legacy_wheel.resolve(strict=True)
    expected=json.loads(args.expected_identity.read_text(encoding='utf-8'))['evaluator']
    assert hashlib.sha256(wheel.read_bytes()).hexdigest()==expected['archive_sha256']
    develop(ROOT,wheel,output/'packages')
    data=output/'data'; parent=output/'workspace'; parent.mkdir()
    report={'claims':'Installed package and simulated-event adapter tests only; no native host, desktop, compaction or resume claim.',
            'candidate_wheel':expected, 'steps':[], 'passed':False}
    env=os.environ.copy(); env.pop('PYTHONPATH',None)
    env.update(PLUGIN_DATA=str(data),CLAUDE_PLUGIN_DATA=str(data),PIP_NO_INDEX='1',PIP_CONFIG_FILE=os.devnull,
               GIT_CONFIG_COUNT='3',GIT_CONFIG_KEY_0='user.name',GIT_CONFIG_VALUE_0='Fixture',
               GIT_CONFIG_KEY_1='user.email',GIT_CONFIG_VALUE_1='fixture@example.invalid',
               GIT_CONFIG_KEY_2='core.autocrlf',GIT_CONFIG_VALUE_2='false')

    def run(label,argv,*,stdin=None,allowed=(0,)):
        begin=time.time()
        result=subprocess.run([str(a) for a in argv],input=stdin,cwd=output,env=env,
            capture_output=True,text=True,encoding='utf-8',timeout=180)
        report['steps'].append({'label':label,'argv':[str(a) for a in argv],'cwd':str(output),
            'exit_code':result.returncode,'seconds':time.time()-begin,'stdout':result.stdout,'stderr':result.stderr})
        (output/'report.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
        assert result.returncode in allowed,(label,result.stdout[-2000:],result.stderr[-2000:])
        return result.stdout

    def hook(host,session,source='startup',cwd=parent):
        script=output/'packages'/host/'verity-plane/scripts/inject_instructions.py'
        raw=run(f'{host}-{session}-{source}',[sys.executable,'-I',script,'--host',host],
            stdin=json.dumps({'hook_event_name':'SessionStart','source':source,'cwd':str(cwd),'session_id':session}))
        return json.loads(raw)['hookSpecificOutput']['additionalContext']

    def activate(host,session,repo=None,allowed=(0,)):
        script=output/'packages'/host/'verity-plane/scripts/activate.py'
        argv=[sys.executable,'-I',script,'--host',host,'--session-id',session,'--data-root',data]
        argv+=['--target',repo] if repo is not None else ['--clear']
        return json.loads(run(f'activate-{host}-{session}',argv,allowed=allowed))

    def prepare(repo,archive,allowed=(0,)):
        script=output/'packages/codex/verity-plane/scripts/setup.py'
        result=run('prepare-'+archive.name,[sys.executable,'-I',script,'--target',repo,'--data-root',data,'--wheel',archive],allowed=allowed)
        found=re.search(r'^Evaluator Python: (.+)$',result,re.M)
        return Path(found[1].strip()) if found else None

    try:
        for host in ('codex','claude'):
            assert '# Select the working repository' in hook(host,host+'-first')
        empty=output/'empty';empty.mkdir()
        python=prepare(empty,wheel,allowed=(1,2))
        assert python and python.is_file()
        assert json.loads((python.parent.parent/'ready.json').read_text())==expected
        remote=output/'fixture-source';remote.mkdir()
        lock={'schema':5,'resource_layout':'released-resources-v1','tool_version':expected['version'],
              'hash_algorithm':'sha256','hash_mode':'utf8-text-lf-v1','evaluator':expected,'files':{}}
        (remote/'.engineering-harness.lock').write_text(json.dumps(lock)+'\n',encoding='utf-8')
        (remote/'.engineering-harness.toml').write_text('[harness]\n'
            f'tool_version = "{expected["version"]}"\nresource_layout = "released-resources-v1"\nproject_name = "Plugin qualification"\n',encoding='utf-8')
        for argv in (['git','-C',remote,'init'],['git','-C',remote,'add','.'],['git','-C',remote,'commit','-m','Disposable selection fixture']):
            run('fixture',argv)
        repo=parent/'cloned'
        run('clone-after-hook',['git','clone',remote,repo])
        assert not (repo/'ENGINEERING_HARNESS.md').exists()
        before={p.name:p.read_bytes() for p in repo.iterdir() if p.is_file()}
        for host in ('codex','claude'):
            session=host+'-first'
            immediate=activate(host,session,repo)
            assert immediate['status']=='available',immediate
            assert '## After compaction' in immediate['content']
            for event in ('compact','resume'):
                text=hook(host,session,event)
                assert str(repo) in text and f'Selected release: {expected["version"]}' in text
                assert text.endswith('A summary preserves pointers and decisions, not current lifecycle truth. Inspect\nuncertain writes or external effects before retrying. Resume only unapplied work.\n')
        assert before=={p.name:p.read_bytes() for p in repo.iterdir() if p.is_file()}
        old=parent/'legacy';old.mkdir()
        old_python=prepare(old,legacy,allowed=(1,2))
        run('legacy-init',[old_python,'-I','-m','se_harness','init',old,'--project-name','Legacy fixture','--json'])
        assert python!=old_python and python.is_file()
        for host in ('codex','claude'):
            activate(host,'parallel',old)
            assert 'Selected release: 0.20.0' in hook(host,'parallel','compact')
            assert f'Selected release: {expected["version"]}' in hook(host,host+'-first','compact')
            assert '# Select the working repository' in hook(host,'independent')
            activate(host,'parallel',repo)
            assert f'Selected release: {expected["version"]}' in hook(host,'parallel','resume')
            activate(host,'parallel')
            assert '# Select the working repository' in hook(host,'parallel')
        # Refuse a failed target and retain the prior successful activation.
        assert activate('codex','codex-first',empty,allowed=(1,))['status']=='unavailable'
        assert str(repo) in hook('codex','codex-first','compact')
        record=data/'sessions/codex'/(hashlib.sha256(b'codex-first').hexdigest()+'.json')
        saved=record.read_bytes();record.write_text('{')
        assert 'delivery is unavailable' in hook('codex','codex-first','compact',old)
        record.write_bytes(saved)
        # Missing and altered cached resources fail without an install or fallback.
        entry=python.parent.parent/'share/se-harness/templates/repository/standard/ENGINEERING_HARNESS.md.tpl'
        original=entry.read_bytes();entry.write_bytes(original+b'\nchanged\n')
        assert 'delivery is unavailable' in hook('codex','codex-first','compact')
        entry.write_bytes(original)
        ready=python.parent.parent/'ready.json';marker=ready.read_bytes();ready.unlink()
        assert 'delivery is unavailable' in hook('claude','claude-first','resume')
        ready.write_bytes(marker)
        # Minimal selection permits delivery; healthy evidence readiness also
        # requires the explicitly selected Git byte-preservation integration.
        integration=[python,'-I','-m','se_harness','upgrade',repo,'--integration','git','--json']
        run('git-integration-preview',integration)
        assert before=={p.name:p.read_bytes() for p in repo.iterdir() if p.is_file()}
        run('git-integration-apply',integration+['--apply'])
        assert {p.name for p in repo.iterdir() if p.is_file()}==set(before)|{'.gitattributes'}
        assert (repo/'.engineering-harness.toml').read_bytes()==before['.engineering-harness.toml']
        integrated_lock=json.loads((repo/'.engineering-harness.lock').read_text(encoding='utf-8'))
        assert integrated_lock['evaluator']==expected
        assert set(integrated_lock['files'])=={'.gitattributes'}
        prepare(repo,wheel)
        assert '## After compaction' in hook('codex','codex-first','compact')
        # Controlled contention: no setup may modify an environment while its lock is held.
        setup_lock=python.parent.parent.with_name(python.parent.parent.name+'.lock')
        setup_lock.write_text('controlled qualification contention')
        try:prepare(repo,wheel,allowed=(1,))
        finally:setup_lock.unlink()
        assert ready.read_bytes()==marker
        report['passed']=True
    finally:
        (output/'report.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'passed':report['passed'],'steps':len(report['steps']),'report':str(output/'report.json')}))


if __name__=='__main__':
    main()
