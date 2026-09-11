"""Run the actual context handler and retain complete output; no authority grant."""
import argparse,json,os,subprocess,hashlib
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--label',required=True);ns=ap.parse_args()
root=Path(__file__).resolve().parent
python=root.parents[1]/'se-harness-plugin-eval-016/Scripts/python.exe'
handler=root.parents[1]/'se-harness-plugin-evidence-skill/plugins/verity-plane/common/scripts/session-context.py'
event=root/(ns.label+'-event.json')
event.write_text(json.dumps({'hook_event_name':'SessionStart','source':'resume','cwd':str(ns.repo)}))
args=[str(python),'-I','-B',str(root/'record_call.py'),'--python',str(python),'--repo',str(ns.repo),'--evidence',str(root/'trace'),'--label',ns.label,'--stdin-file',str(event),'--native','--',str(python),'-I','-B',str(handler),'--repo',str(ns.repo),'--environment',str(python.parent.parent),'--version','0.16.0','--payload-sha256','51712fcfe5253db8d542deb870a0017b25c2976f5f4e76a81fd08923bba45e3c','--archive-sha256','a969d6ab9e80acc2c9f9e7b6679a02e7ffab371f1f11cb0c0f4243f208ed9eae','--host','codex','--context-limit','32768','--read-limit','32768']
r=subprocess.run(args,capture_output=True,cwd=root)
row=json.loads((root/'trace'/(ns.label+'.json')).read_text())
current=json.loads(row['stdout'])['hookSpecificOutput']['additionalContext']
prior=json.loads(json.loads((root/'trace/setup-15-context.json').read_text())['stdout'])['hookSpecificOutput']['additionalContext']
print(json.dumps({'record':ns.label,'repository':str(ns.repo),'exit_code':row['exit_code'],'complete_output_identical_to_already_read_body':current==prior,'full_body_sha256':hashlib.sha256(current.encode()).hexdigest(),'marker':current.strip().splitlines()[-1],'changed_paths':row['changed_paths']}))
if current!=prior:print(current)
