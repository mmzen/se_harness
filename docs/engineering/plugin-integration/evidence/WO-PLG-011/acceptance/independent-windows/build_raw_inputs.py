"""Author fixed synthetic starting artifacts only; no evaluator replacement."""
import hashlib, json
from pathlib import Path

ROOT=Path(__file__).resolve().parent
ASSETS=ROOT/'raw-assets'
def write(path,text):
    p=ASSETS/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text,encoding='utf8')
def formal(kind,prefix,status,owner,relations,body,extra=''):
    text=f'+++\nid = "{prefix}-EVD-001"\ntype = "{kind}"\ntitle = "Evidence preparation fixture {prefix}"\nstatus = "{status}"\nowners = ["{owner}"]\ncreated = "2026-09-10"\nupdated = "2026-09-10"\n{extra}\n[relations]\n'
    text+=''.join(f'{k} = {json.dumps(v)}\n' for k,v in relations.items())
    return text+'+++\n\n'+body+'\n'
base='docs/engineering/evidence-demo/'
write(Path(base+'intent/INT-EVD-001.md'),formal('intent','INT','approved','product-owner',{},'# Intent\n\nRetain observable evidence for bounded local work.'))
write(Path(base+'capabilities/CAP-EVD-001.md'),formal('capability','CAP','approved','product-owner',{'derives_from':['INT-EVD-001']},'# Capability\n\nInspect one implemented candidate.'))
write(Path(base+'requirements/REQ-EVD-001.md'),formal('requirement','REQ','approved','product-owner',{'derives_from':['CAP-EVD-001']},'# Requirement\n\nThe local fixture reports the fixed greeting.', 'statement = "WHEN invoked, THE SYSTEM SHALL return the greeting Hello evidence."\nverification_method = ["automated-test"]'))
write(Path(base+'specifications/SPEC-EVD-001.md'),formal('specification','SPEC','approved','technical-owner',{'specifies':['REQ-EVD-001']},'# Specification\n\nThe fixture feature returns Hello evidence. No external action is performed.'))
write(Path(base+'verification/VER-EVD-001.md'),formal('verification','VER','approved','assurance-owner',{'verifies':['REQ-EVD-001']},'# Verification contract\n\nIndependently assert exact greeting Hello evidence. A separate injected failing probe and unrun probe test truthful evidence retention; they are not candidate acceptance criteria.'))
wo_extra='''
[assurance]
commit_bound_verification = "required"
rationale = "The fixture captures exact committed implementation evidence."
decided_by = "engineering-owner"

[execution_scope]
paths = ["src/feature.py", "docs/engineering/evidence-demo/work-orders/WO-EVD-001.md", "docs/engineering/evidence-demo/evidence/WO-EVD-001/"]
'''
wo_body='''# Work order

## Objective

Retain the greeting implementation and its actual local evidence.

## In scope

The feature file and this work order's evidence directory.

## Out of scope

Every source worktree and every real external action.

## Authorized decision envelope

Synthetic preexisting engineering-owner approval, start and completion form the initial implemented fixture state. They authorize no assurance, release, or external action.

## Stop conditions

Missing authority, unavailable current context, changed inputs or a failed required gate.

## Required verification

Exact greeting assertion, actual installed doctor and selected review preflight.

## Completion report format

Report observed commands, effects, selected state and typed next action.
'''
write(Path(base+'work-orders/WO-EVD-001.md'),formal('work_order','WO','implemented','engineering-owner',{'implements':['REQ-EVD-001'],'specifications':['SPEC-EVD-001'],'verification':['VER-EVD-001']},wo_body,wo_extra))
write(Path(base+'release/REL-EVD-001.md'),formal('release_contract','REL','approved','release-owner',{'gates':['WO-EVD-001']},'# Release contract\n\nRelease preparation includes one verified candidate, its work order and exact version. Publication requires a separate exact action decision and independent controls.'))
write(Path('src/feature.py'),'def greeting():\n    return "Hello evidence"\n')
write(Path(base+'evidence/WO-EVD-001/observations.md'),'# Retained candidate evidence\n\nInitial fixture has no claimed verification result. Actual observations are retained before capture.\n')
manifest={p.relative_to(ASSETS).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(ASSETS.rglob('*')) if p.is_file()}
(ROOT/'raw-assets-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps(manifest,indent=2))
