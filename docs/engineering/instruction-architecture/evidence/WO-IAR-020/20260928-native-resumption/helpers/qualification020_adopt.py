"""Apply only the reviewed 0.2.0 local-marketplace adoption via host commands."""
import datetime,hashlib,json,os,subprocess,sys
from pathlib import Path
WORK=Path(__file__).resolve().parent
OUT=WORK/'qualification020-adoption';OUT.mkdir(exist_ok=True)
REPO=WORK/'se_harness'
REVIEW=REPO/'docs/engineering/instruction-architecture/acceptance/plugin-adoption/replacement.json'
plan=json.loads(REVIEW.read_text(encoding='utf-8'))
HOSTS={'codex':r'C:\Users\mathi\AppData\Local\OpenAI\Codex\bin\faa963e871dd422c\codex.exe','claude':r'C:\Users\mathi\.local\bin\claude.exe'}

def save(name,value):
    p=OUT/(name+'.json')
    if p.exists():raise RuntimeError('Inspect prior effects before retry: '+str(p))
    p.write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

def call(label,host,args):
    argv=[HOSTS[host],*args]
    if (OUT/(label+'.json')).exists():raise RuntimeError('Inspect prior effects before retry: '+label)
    p=subprocess.run(argv,cwd=OUT,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=120)
    try:result=json.loads(p.stdout)
    except ValueError:result=p.stdout.strip()
    save(label,{'argv':argv,'cwd':str(OUT),'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'exit_code':p.returncode,'result':result,'stderr':p.stderr})
    print(json.dumps({'label':label,'exit_code':p.returncode,'result':result if len(json.dumps(result))<2000 else 'Full result retained in '+str(OUT/(label+'.json'))}),flush=True)
    if p.returncode:raise RuntimeError(label+' failed; inspect actual effects before retry')
    return result

def review_bytes():
    for host,info in plan['hosts'].items():
        root=Path(info['package'])
        assert hashlib.sha256((root/'assembly-inventory.json').read_bytes()).hexdigest()==info['assembly_inventory_sha256']
        for rel,row in info['files'].items():assert hashlib.sha256((root/rel).read_bytes()).hexdigest()==row['sha256'],(host,rel)
    for rel,digest in plan['marketplace_files'].items():assert hashlib.sha256((Path(plan['marketplace'])/rel).read_bytes()).hexdigest()==digest

mode=sys.argv[1]
if mode=='inventory':
    review_bytes()
    for host in HOSTS:
        call(host+'-marketplaces-before',host,['plugin','marketplace','list','--json'])
        call(host+'-plugins-before',host,['plugin','list','--json'])
    save('review',{'reviewed_manifest':str(REVIEW),'reviewed_manifest_sha256':hashlib.sha256(REVIEW.read_bytes()).hexdigest(),'all_bytes_match':True,'target_version':'0.2.0','selected_evaluator_unchanged':'0.19.0','authority':'Human mmzen: Go, continuing the reviewed native qualification and real-profile adoption handoff. Scope is only the se-harness source and verity-plane@se-harness 0.2.0; hook trust is through supported host review.'})
elif mode in ('adopt','replace'):
    host=sys.argv[2]
    assert host in HOSTS
    assert json.loads((OUT/'review.json').read_text(encoding='utf-8'))['all_bytes_match']
    boundary=json.loads((WORK/'qualification020-host/claude-boundaries-assessment.json').read_text(encoding='utf-8'))
    assert boundary['cases'][0]['case']=='switch' and boundary['cases'][0]['passed']
    assert json.loads((WORK/'qualification020-host/claude-behavior-boundaries-assessment.json').read_text(encoding='utf-8'))['status']=='passed'
    assert json.loads((WORK/'qualification020-host/claude-compact-assessment.json').read_text(encoding='utf-8'))['passed']
    review_bytes()
    if mode=='replace':
        current=call(host+'-before-replacement',host,['plugin','marketplace','list','--json'])
        markets=current['marketplaces'] if host=='codex' else current
        selected=[m for m in markets if m['name']=='se-harness']
        assert len(selected)==1
        if host=='codex':assert selected[0]['marketplaceSource']=={'sourceType':'git','source':'https://github.com/mmzen/se_harness.git'}
        else:assert selected[0]['repo']=='mmzen/se_harness' and selected[0]['ref']=='plugin-marketplace'
        call(host+'-marketplace-remove-old',host,['plugin','marketplace','remove','se-harness',*(['--json'] if host=='codex' else ['--scope','user'])])
    # Each host's supported add command handles an existing marketplace name.
    call(host+'-marketplace-'+('replace' if mode=='replace' else 'adopt'),host,['plugin','marketplace','add',plan['marketplace'],*(['--json'] if host=='codex' else ['--scope','user'])])
    call(host+'-plugin-adopt',host,['plugin',('add' if host=='codex' else 'install'),'verity-plane@se-harness',*(['--json'] if host=='codex' else ['--scope','user','--json'])])
    call(host+'-plugins-after',host,['plugin','list','--json'])
    call(host+'-marketplaces-after',host,['plugin','marketplace','list','--json'])
