# Guide-retirement acceptance boundary

The product stops distributing and creating these six owner seeds:

| Retired file under docs/engineering/ | Current instructions under harness/ |
| --- | --- |
| OPERATING_CARD.md | CONTINUE.md |
| DECISION_RIGHTS.md | AUTHORITY.md |
| QUALITY_GATES.md | RESULTS.md |
| WORKFLOW.md | CONTINUE.md, RECORD_STATE.md, RESULTS.md |
| TRACEABILITY.md | ARTIFACTS.md, DEFINITION_LINKS.md, WORK_AND_EVIDENCE.md |
| TECHNICAL_COMMUNICATION.md | COMMUNICATION.md |

Existing 0.19.0 owner files remain byte-identical and leave the lock. Absent
files stay absent. Supported 0.18.0 full guides convert only through the
recognized migration or an explicitly authorized replacement; custom inputs
otherwise refuse before writes.

The implementation assessment and retained observations are in
[the review](../../evidence/WO-IAR-022/review.md). Verification covers
WO-IAR-022/024/025 under VER-IAR-017. A ready VREC is not human acceptance.

This repository's installed six pointers are not removed. Real cleanup waits
for native qualification under WO-IAR-020, an exact published release, a current
consumer review and a separately approved adoption. Use the product procedure
in harness/UPGRADE.md#separately-authorized-pointer-cleanup for that later action.
