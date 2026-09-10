"""Fix supplied package input bytes before its behavioral create test."""
import hashlib
import json
from pathlib import Path
root=Path(__file__).resolve().parent
inputs=root/'package-inputs'
inputs.mkdir(exist_ok=False)
spec='''+++
id = "SPEC-PKG-001"
type = "specification"
title = "Clear feature message"
status = "draft"
owners = ["technical-owner"]
created = "2026-09-10"
updated = "2026-09-10"
contract = "The feature displays one short English message."

[relations]
specifies = ["REQ-ACC-001"]
+++

# Specification: Clear feature message

## In plain words

Operators read a clear status message.

## Scope

The wording returned by the feature.

## Terms

None.

## Rules

**PKG-MSG-001.** The feature MUST return one short English message.

## Failure behaviour

| Trigger | Response | Diagnostic |
| --- | --- | --- |
| Message unavailable | Return a short error message | Message unavailable |

## Examples

**Given** a working feature, **when** requested, **then** a message is returned under PKG-MSG-001.

## Coverage

| Requirement | Rules |
| --- | --- |
| `REQ-ACC-001` | PKG-MSG-001 |

## Not decided here

- The punctuation selected by the open decision.
'''
wo=(root/'raw-repository/docs/engineering/acceptance/work-orders/WO-ACC-001.md').read_text()
wo=wo.replace('WO-ACC-001','WO-PKG-001').replace('SPEC-ACC-001','SPEC-PKG-001').replace('docs/engineering/acceptance/','docs/engineering/package-demo/').replace('src/feature.py','src/package_feature.py')
decision='''+++
id = "DEC-PKG-001"
type = "decision"
title = "Message punctuation"
status = "open"
owners = ["engineering-owner"]
created = "2026-09-10"
updated = "2026-09-10"
kind = "question"
question = "Should the message end with a period?"
raised_by = "fixture-author"
recommendation = "period"

[[options]]
id = "period"
label = "Use a period"

[[options]]
id = "plain"
label = "Use no punctuation"

[relations]
concerns = ["WO-PKG-001"]
blocks = ["WO-PKG-001"]
+++

# Decision: Message punctuation

The engineering owner selects the punctuation before approving the work order.
'''
for name,content in [('SPEC-PKG-001.md',spec),('WO-PKG-001.md',wo),('DEC-PKG-001.md',decision)]:
    (inputs/name).write_text(content,encoding='utf8')
(inputs/'request.json').write_text(json.dumps({
    'fixture_only':True,'request':'Create the package-demo domain and the three supplied records. Complete their supplied content. This authoring request contains no lifecycle approvals or decision disposition.',
    'raw_paths':{name:hashlib.sha256((inputs/name).read_bytes()).hexdigest() for name in ['SPEC-PKG-001.md','WO-PKG-001.md','DEC-PKG-001.md']},
    'decisions':[],
    'interruption':'Suppress the receipt after the first successful create; then resume the same request using actual readback.'
},indent=2)+'\n')
print((inputs/'request.json').read_text())
