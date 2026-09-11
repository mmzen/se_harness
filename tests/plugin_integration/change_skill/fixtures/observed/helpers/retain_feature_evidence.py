"""Append only observed results; never prepare or assert future outcomes."""
import json
from pathlib import Path
import sys
root=Path(__file__).resolve().parent
repo=Path(sys.argv[1])
path=repo/'docs/engineering/demo-change/evidence/WO-ACC-001/WO-ACC-001-handoff.md'
lines=['\n## Observed fixture outcomes\n',
       'Two authorized feature edits were committed locally. The work order remains in_progress.\n']
for label in ('chg04-observed-feature','chg04-review-preflight','chg04-validate','chg04-doctor'):
    result=json.loads((root/'behavior-evidence'/(label+'.json')).read_text())
    lines.append(f'- {label}: actual process exit {result["exit_code"]}.\n')
lines.append('\nThe observed message was: The feature is ready to use.\n')
lines.append('Original per-edit pre-action attempts failed QGP-G4I-EVIDENCE and are retained outside this fixture repository.\n')
lines.append('No completion, assurance, release, push, merge, or live CI result is asserted here.\n')
with path.open('a',encoding='utf8') as stream:
    stream.write(''.join(lines))
