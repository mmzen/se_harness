+++
id = "DEC-IAR-003"
type = "decision"
title = "Set the release boundary for external harness resources"
status = "decided"
owners = ["mmzen"]
created = "2026-09-30"
updated = "2026-09-30"
kind = "question"
question = "May the external-resource package govern a future released layout under the explicit applicability map, while preserving old definitions and the installed 0.20.0 rules until separate adoption?"
raised_by = "Codex drafting agent"
recommendation = "versioned-successor"

[[options]]
id = "versioned-successor"
label = "Use the reviewed future-release boundary and preserve accepted history."

[[options]]
id = "await-revision-capability"
label = "Keep the package in draft pending supported linked revision and activation."

[relations]
concerns = ["REQ-IAR-029", "REQ-IAR-030", "REQ-IAR-031", "SPEC-IAR-016", "ARCH-IAR-012", "ADR-IAR-012", "VER-IAR-020", "VER-IAR-021", "VER-IAR-022", "WO-IAR-028", "WO-IAR-029", "WO-IAR-030", "SPEC-IAR-014", "REQ-IAR-022", "REQ-IAR-024", "REQ-IAR-026", "SPEC-DST-002", "SPEC-DST-028", "REQ-PLG-010", "SPEC-PLG-007", "REQ-AUT-001", "SPEC-AUT-001", "SPEC-IAR-006", "SPEC-IAR-015"]
blocks = ["REQ-IAR-029", "REQ-IAR-030", "REQ-IAR-031", "SPEC-IAR-016", "ARCH-IAR-012", "ADR-IAR-012", "VER-IAR-020", "VER-IAR-021", "VER-IAR-022", "WO-IAR-028", "WO-IAR-029", "WO-IAR-030"]

[disposition]
option = "versioned-successor"
label = "Use the reviewed future-release boundary and preserve accepted history."
decided_by = "mmzen"
decided_at = "2026-09-30T09:39:09Z"
reason = "Future release and separate adoption (Recommended)."

[[lifecycle_events]]
from = "open"
to = "decided"
decided_at = "2026-09-30T09:39:09Z"
decided_by = "mmzen"
reason = "Future release and separate adoption (Recommended)."
+++

# Set the release boundary for external harness resources

## Question and current boundary

The owner accepted the objective and requested these drafts. This does not by
itself approve a work order or redefine accepted installed-file requirements.
0.20.0 has no supported generic linked-revision activation command. This decision
therefore blocks the proposed implementation until the human explicitly accepts
the future-release applicability boundary or chooses to wait.

## Proposed applicability map

| Existing obligation | Future-release treatment |
| --- | --- |
| SPEC-IAR-014 IAR-DIS-001, 002 and 008; REQ-IAR-022/026 entry delivery | Preserve compact entry content and native startup/compaction, but resolve the entry from the selected wheel rather than require a repository root file. |
| SPEC-IAR-014 IAR-DIS-004/005 and REQ-IAR-024 discovery | Preserve evaluator-selected steps and machine-only policy reads; explicitly version the resource-location result instead of interpreting an old relative-file result differently. |
| SPEC-IAR-014 IAR-DIS-010/013 ownership and migration | Preserve one canonical source and rule coverage; move standard material into the released payload, preserve customized owner material and historical records. |
| SPEC-DST-002 and SPEC-DST-028 repository copies/templates | Existing historical deliveries remain valid. The new standard layout uses packaged templates and an explicit safe migration instead of creating copies. Earlier AGENTS-gate requirements remain historical, not revived. |
| REQ-AUT-001 and SPEC-AUT-001 AUT-POL-001/003/005 | Preserve one canonical authoring policy, selected type checklists and required readiness; the successor reads the released package instead of requiring or reading a repository copy. Do not revive superseded writing-shape rules. |
| SPEC-IAR-006 authoring locations | Preserve artifact types, applicability and authoring mechanics. Expose their current packaged destinations instead of requiring a templates/README.md copy. |
| SPEC-IAR-015 IAR-RET-006 cleanup exclusions | The completed six-pointer cleanup remains unchanged. Its preservation boundary does not itself authorize this broader migration; only the new reviewed release/adoption can retire the remaining stock resources. |
| REQ-PLG-010 / SPEC-PLG-007 older host context | Preserve identity and delivery obligations under their recorded versions; new host adapters select the layout explicitly and retain supported 0.20.0 behavior. |

## Options

**versioned-successor:** Accept this package as the contract for a future
released layout. Preserve the old records and their past work/evidence. Keep the
installed 0.20.0 route until separate release/adoption, with explicit compatibility
and resource identity. This is not a generic supersedes relation, a silent amendment
or permission to weaken required gates. Review the stated map before approval.

**await-revision-capability:** Keep this package in draft until a separately
governed release provides supported linked-definition revision and activation.
This avoids an applicability decision now but delays the requested evolution.

## Recommendation and KIS rationale

Choose versioned-successor, subject to explicit human confirmation. It uses the
existing release/adoption boundary rather than adding a generic revision feature
to a resource-location change. DEC-IAR-001 records a similar earlier decision;
its scope does not automatically authorize this one.

The wheel-carrier design is recorded once in ADR-IAR-012; this DEC only resolves
formal applicability. Ordinary implementation choices do not get extra decisions.
Approval and required assurance for WO-IAR-028, WO-IAR-029, WO-IAR-030 remain separate.

## Reviewed accepted versions

The full file-byte digests identify the accepted records considered by this
applicability proposal. Their content and lifecycle remain unchanged.

| Artifact | State | SHA-256 |
| --- | --- | --- |
| SPEC-IAR-014 | approved | `b020c04570cc083c3eaa77622c4326c15b62ac7ed82a7efe69a671212e6bffb6` |
| REQ-IAR-022 | approved | `66984604a2c49a54502b52d52fa4bfe80c951ca8c02f9487c626c054d06645f5` |
| REQ-IAR-024 | approved | `ab9dfacfa1031214d603fc67ed7c941b5abe8bc6e6e0bfb7f037528fbb5a1f2c` |
| REQ-IAR-026 | approved | `1b7bf8d5060e98d248fbbfca0613f8497e91189030df4420080c7b456338360c` |
| SPEC-DST-002 | implemented | `339fee49ed97eebddeab5a08fa20187bf30aa9870b64a2e2c56f53e05a1b4a14` |
| SPEC-DST-028 | approved | `3af879569ab1a902a4531bf12e4b54e4004e90a3068271d659c225cb65b8b92e` |
| REQ-PLG-010 | approved | `74002fa7b7657179d4f1089205d58ca32b250ec30f2cad118d0c0e59dde27848` |
| SPEC-PLG-007 | approved | `cae3a165cf15d6691fd24b3d78b75f071a8227a361b4071682b9fc46a239b21f` |
| REQ-AUT-001 | approved | `347e1b71b326971e654536f503b70a1914f9b3683151e1c42740e697b5662969` |
| SPEC-AUT-001 | approved | `f2651adb44054ee2b9ce5b8303c30f0474b0af54d2dca9b06e6b354169ee0ff1` |
| SPEC-IAR-006 | implemented | `9b18e5fd2d82b6a6910fd32e04c0bfeb532dd6fcf00e35da551982e8b0b00546` |
| SPEC-IAR-015 | approved | `063e0e767784a80c701755ccfcdfe96549046a030ac02cbeb14b8494d8659af0` |
