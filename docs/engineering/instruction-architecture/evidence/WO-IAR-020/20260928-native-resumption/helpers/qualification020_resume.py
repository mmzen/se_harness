import datetime,hashlib,json,subprocess,sys
from pathlib import Path
WORK=Path(__file__).resolve().parent
OUT=WORK/(sys.argv[2] if len(sys.argv)>2 else 'qualification020-resume');OUT.mkdir(exist_ok=True)
sys.path.insert(0,str(WORK/'iar-demo-tools'))
import run_demo
from acceptance_native import claude_probe,assess,snapshot
manifest=json.loads((WORK/'iar-demo-tools/prepared-demo.json').read_text(encoding='utf-8'))
manifest['host_executables']={'claude':r'C:\Users\mathi\.local\bin\claude.exe','codex':r'C:\Users\mathi\AppData\Local\OpenAI\Codex\bin\faa963e871dd422c\codex.exe'}
env=run_demo.child_env(Path(manifest['demo']),'claude')
exe=manifest['host_executables']['claude']
assert 'iar-instruction-demo-' in env['CLAUDE_CONFIG_DIR']
def save(name,value):
    path=OUT/name
    if path.exists():raise RuntimeError('Inspect previous output before retry: '+str(path))
    path.write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def command(label,args,environment=None):
    p=subprocess.run(list(map(str,args)),cwd=OUT,env=environment,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=90)
    try:v=json.loads(p.stdout)
    except ValueError:v=p.stdout.strip()
    result={'argv':list(map(str,args)),'cwd':str(OUT),'exit_code':p.returncode,'result':v,'stderr':p.stderr}
    save(label+'.json',result)
    print(json.dumps({'label':label,'exit_code':p.returncode,'result':v}),flush=True)
    return p.returncode,v
if sys.argv[1]=='inspect':
    proposal=json.loads((WORK/'se_harness/docs/engineering/instruction-architecture/acceptance/plugin-adoption/replacement.json').read_text(encoding='utf-8'))
    for host,info in proposal['hosts'].items():
        p=Path(info['package'])
        assert hashlib.sha256((p/'assembly-inventory.json').read_bytes()).hexdigest()==info['assembly_inventory_sha256']
        for rel,row in info['files'].items():assert hashlib.sha256((p/rel).read_bytes()).hexdigest()==row['sha256'],(host,rel)
    for rel,digest in proposal['marketplace_files'].items():assert hashlib.sha256((Path(proposal['marketplace'])/rel).read_bytes()).hexdigest()==digest
    save('package-review.json',{'observed_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'all_reviewed_bytes_match':True,'target_version':proposal['target_version'],'marketplace':proposal['marketplace'],'selected_evaluator_remains':proposal['selected_evaluator_remains']})
    for host,host_exe in manifest['host_executables'].items():
        command(host+'-version',[host_exe,'--version'])
        command(host+'-real-plugins',[host_exe,'plugin','list','--json',*(['--marketplace','se-harness'] if host=='codex' else [])])
    command('claude-isolated-plugins',[exe,'plugin','list','--json'],env)
    p=subprocess.run([exe,'auth','status','--json'],env=env,cwd=OUT,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=90)
    try:status=json.loads(p.stdout)
    except ValueError:status={'status_parse_failed':True}
    safe={k:status[k] for k in ['loggedIn','authMethod','apiProvider','subscriptionType','status_parse_failed'] if k in status}
    result={'argv':[exe,'auth','status','--json'],'profile':env['CLAUDE_CONFIG_DIR'],'exit_code':p.returncode,'status':safe}
    save('claude-auth-status.json',result);print(json.dumps(result),flush=True)
elif sys.argv[1]=='auth':
    p=subprocess.run([exe,'auth','status','--json'],cwd=OUT,env=env,capture_output=True,text=True,encoding='utf-8',timeout=90)
    status=json.loads(p.stdout)
    print(json.dumps({'exit_code':p.returncode,'profile':env['CLAUDE_CONFIG_DIR'],'status':{k:status[k] for k in ['loggedIn','authMethod','apiProvider','subscriptionType'] if k in status}}),flush=True)
elif sys.argv[1]=='login':
    print('Renewing only the isolated Claude profile: '+env['CLAUDE_CONFIG_DIR'],flush=True)
    raise SystemExit(subprocess.call([exe,'auth','login','--claudeai'],cwd=OUT,env=env))
elif sys.argv[1]=='startup':
    target=WORK/'cleanup-native/claude-repository'
    trace=OUT/'claude-startup';trace.mkdir(exist_ok=False)
    report={'host':'claude','profile':env['CLAUDE_CONFIG_DIR'],'repository':str(target),'status':'incomplete','cases':[]}
    try:
        session,contexts,replies=claude_probe(manifest,target,trace,'startup')
        result=assess(target,contexts,replies)
        report.update(status='passed' if result['passed'] else 'failed',session_id=session)
        report['cases'].append({'phase':'startup',**result})
    except Exception as exc:report['error']=str(exc)
    save('claude-startup.json',report)
    print(json.dumps({'status':report['status'],'error':report.get('error'),'cases':report['cases']}),flush=True)
