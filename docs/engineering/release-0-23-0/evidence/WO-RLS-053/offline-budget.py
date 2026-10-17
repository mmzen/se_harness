"""Offline review only: run the unchanged launcher's pre-provider input assembly."""
import argparse,ast,copy,hashlib,json,shutil,sys,zipfile
from pathlib import Path
import hag_efficiency_plan as p
O=p.W/'release023-053-proposal';Q=p.W/'release023-052-qualification'
attempt=sys.argv[1] if len(sys.argv)>1 else ''
sys.path.insert(0,str(p.R/'tests/hosted_artifact_graph'))
import qualify_agents as q
sha=lambda b:hashlib.sha256(b).hexdigest()
load=lambda f:json.loads(f.read_text(encoding='utf-8-sig'))
selectors=['docs/engineering/harness/COMMUNICATION.md#communication',
 'docs/engineering/harness/DRAFT_DEFINITIONS.md#read-this-when',
 'docs/engineering/harness/DRAFT_DEFINITIONS.md#before-this-action',
 'docs/engineering/harness/DRAFT_DEFINITIONS.md#define-how-the-result-will-be-verified',
 'docs/engineering/harness/ARTIFACTS.md#artifact-types',
 'docs/engineering/harness/ARTIFACTS.md#artifact-locations',
 'docs/engineering/harness/DEFINITION_LINKS.md#links-between-definitions',
 'docs/engineering/ARTIFACT_AUTHORING.md#design-simplicity',
 'docs/engineering/ARTIFACT_AUTHORING.md#verification']

# Include the original complete-input guard. Exclude all provider/network/capture
# code after it. Trace reads locals only; it does not alter assembly or limits.
path=Path(q.__file__);tree=ast.parse(path.read_text());fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='run')
cut=next(i for i,n in enumerate(fn.body) if isinstance(n,ast.If) and isinstance(n.test,ast.Name) and n.test.id=='entry')
fn=copy.deepcopy(fn);fn.body=fn.body[:cut]
module=ast.Module(body=[fn],type_ignores=[]);scope=dict(vars(q))
exec(compile(ast.fix_missing_locations(module),str(path),'exec'),scope)
results=[]
for host in ('claude','codex'):
 for variant in ('accepted','proposed'):
  source=Q/'native/claude-positive1/native';root=O/f'offline{attempt}-{host}-{variant}'/'native'
  root.mkdir(parents=True,exist_ok=False);shutil.copytree(source/'inputs',root/'inputs');(root/'work').mkdir()
  if host=='codex':
   # Replace the Claude package with the exact previously built Codex package.
   # No recursive deletion: a same-path overlay contains shared identical files;
   # remove only files exclusive to Claude's plugin metadata after inspection.
   with zipfile.ZipFile(Q/'combination/plugin/verity-plane-codex.zip') as z:
    allowed={i.filename for i in z.infolist() if not i.is_dir()}
    assert all(not Path(n).is_absolute() and '..' not in Path(n).parts for n in allowed)
    plugin=root/'inputs/plugin'
    for f in plugin.rglob('*'):
     if f.is_file() and f.relative_to(plugin).as_posix() not in allowed:f.unlink()
    z.extractall(plugin)
  if variant=='proposed':
   for name in ('native-tools','native-execution-tools'):
    (root/'inputs'/f'{name}.md').write_bytes((O/f'{name}-proposed.txt').read_bytes())
  settings=load(source/'selection.json')
  def relocate(value):
   if isinstance(value,str):
    for a,b in ((str(source),str(root)),(source.as_posix(),root.as_posix()),(source.as_posix().replace('C:','//c'),root.as_posix().replace('C:','//c'))):value=value.replace(a,b)
    return value
   if isinstance(value,list):return [relocate(x) for x in value]
   if isinstance(value,dict):return {k:relocate(v) for k,v in value.items()}
   return value
  settings=relocate(settings);settings['host']=host
  if host=='codex':
   old=load(p.W/'h44/e/codex-432/native-selection.json')
   # Preserve the native Codex prefix shape; relocate only its selected workspace.
   oldroot=p.W/'h44/e/codex-432/native'
   settings['approved_shell_argv_prefix']=[v.replace(str(oldroot),str(root)).replace(oldroot.as_posix(),root.as_posix()) for v in old['approved_shell_argv_prefix']]
  selected=root.parent/'selected.json';selected.write_text(json.dumps(settings,indent=2)+'\n')
  inventory=Path(settings['inputs_inventory']);files=[]
  for f in sorted((root/'inputs').rglob('*')):
   if f.is_file() and f!=inventory:files.append({'path':str(f),'relative':f.relative_to(root/'inputs').as_posix(),'bytes':len(f.read_bytes()),'sha256':sha(f.read_bytes())})
  inventory.write_text(json.dumps({'files':files},indent=2)+'\n')
  original=p.W/f'h44/e/{host}-432/native-task.md';task=original.read_text()
  oldroot=p.W/f'h44/e/{host}-432/native'
  for a,b in ((str(oldroot),str(root)),(oldroot.as_posix(),root.as_posix()),(oldroot.as_posix().replace('C:','//c'),root.as_posix().replace('C:','//c'))):task=task.replace(a,b)
  taskfile=root.parent/'request.md';taskfile.write_text(task,encoding='utf-8',newline='\n')
  credentials=root.parent/'synthetic-credentials.json';credentials.write_text(json.dumps({'principals':[{'id':'operator','token':'offline-synthetic-credential-not-for-network'}]}))
  args=argparse.Namespace(output=root,prepared_inputs=True,selection=selected,credentials=credentials,host=host,
     drop_reply=False,complete_inputs=True,instruction_section=selectors,task=taskfile,codex_loopback_network=False)
  captured={}
  def trace(frame,event,arg):
   if frame.f_code.co_name=='run' and 'prompt' in frame.f_locals:
    captured.update({k:frame.f_locals[k] for k in ('prompt','entry','settings') if k in frame.f_locals})
   return trace
  sys.settrace(trace)
  error=None
  try:scope['run'](args)
  except ValueError as exc:error=str(exc)
  finally:sys.settrace(None)
  prompt=captured['prompt'];packet=captured['entry']
  sourcefiles=packet['complete_input_files']['sources']
  expected={f.relative_to(source/'inputs/source').as_posix():sha(f.read_bytes()) for f in (source/'inputs/source').rglob('*') if f.is_file()}
  actual={Path(item['path']).relative_to(root/'inputs/source').as_posix():sha(item['text'].encode()) for item in sourcefiles}
  assert expected==actual
  originals=[{'relative':n,'sha256':s} for n,s in sorted(expected.items())]
  row={'host':host,'variant':variant,'root':str(root),'root_characters':len(str(root)),
   'prompt_bytes':len(prompt.encode()),'headroom_bytes':65536-len(prompt.encode()),'error':error,
   'source_files':originals,'source_bytes':packet['source_bytes'],'reference_bytes':packet['reference_bytes'],
   'selected_sections':selectors,'task_source':str(original),'original_task_sha256':sha(original.read_bytes()),
   'assembled_task_sha256':sha(prompt.encode()),'qualifier_sha256':sha(path.read_bytes()),
   'guide_sha256':sha((root/'inputs/native-tools.md').read_bytes()),
   'provider_invoked':False,'service_contacted':False,'method':'Unchanged run() statements through the 64 KiB/credential guard, with provider/capture code excluded by AST boundary; no prompt substitution.'}
  (root.parent/'measurement.json').write_text(json.dumps(row,indent=2)+'\n');results.append(row)
  print(json.dumps({k:row[k] for k in ('host','variant','root_characters','prompt_bytes','headroom_bytes','error')}),flush=True)
(O/f'offline-budget{attempt}.json').write_text(json.dumps({'basis':'b9620f58ab018d75a463b38c34422371874778e8','results':results},indent=2)+'\n')
assert all(r['error'] is None for r in results if r['variant']=='proposed')
