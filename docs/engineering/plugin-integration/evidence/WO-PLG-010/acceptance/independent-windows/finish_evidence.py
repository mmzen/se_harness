"""Derive readable diffs and an inventory from actual retained fixture bytes."""
import difflib
import hashlib
import json
from pathlib import Path
root=Path(__file__).resolve().parent
out=root/'behavior-evidence'
paths=['docs/engineering/package-demo/specifications/SPEC-PKG-001.md','docs/engineering/package-demo/work-orders/WO-PKG-001.md','docs/engineering/package-demo/decisions/DEC-PKG-001.md']
diff=['Derived from recorded absence before create and actual final fixture bytes.\n']
for rel in paths:
    diff.extend(difflib.unified_diff([], (root/'behavior3-repository'/rel).read_text().splitlines(keepends=True),fromfile='/dev/null',tofile=rel))
(out/'chg01-diff.txt').write_text(''.join(diff),encoding='utf8')
before=root/'raw-repository/docs/engineering/acceptance/intent/INT-ACC-001.md'
after=root/'transition-repository/docs/engineering/demo-change/intent/INT-ACC-001.md'
(out/'chg08-diff.txt').write_text('Derived from fixed reviewed bytes and actual readback after suppressed receipt.\n'+''.join(difflib.unified_diff(before.read_text().splitlines(keepends=True),after.read_text().splitlines(keepends=True),fromfile='reviewed/INT-ACC-001.md',tofile='observed/INT-ACC-001.md')),encoding='utf8')
for moment in ('before','after'):
    row=json.loads((out/('chg10-repeat-state-'+moment+'.json')).read_text())
    (out/('chg10-state-'+moment+'.json')).write_text(json.dumps(json.loads(row['stdout']),indent=2)+'\n',encoding='utf8')
manifest={p.relative_to(root).as_posix():hashlib.sha256(p.read_bytes()).hexdigest()
          for folder in [out,root/'candidate',root/'candidate-corrected',root/'package-inputs']
          for p in sorted(folder.rglob('*')) if p.is_file()}
for name in ('REPORT.md','oracle.md','fixed-inputs.json','trace-groups.json'):
    manifest[name]=hashlib.sha256((root/name).read_bytes()).hexdigest()
(root/'evidence-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf8')
print(json.dumps({'retained_files':len(manifest),'report_sha256':manifest['REPORT.md'],'manifest_sha256':hashlib.sha256((root/'evidence-manifest.json').read_bytes()).hexdigest()},indent=2))
