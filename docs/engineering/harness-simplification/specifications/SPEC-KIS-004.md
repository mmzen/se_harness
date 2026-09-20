+++
id = "SPEC-KIS-004"
type = "specification"
title = "Keep evidence outcomes truthful"
status = "approved"
owners = ["technical-owner"]
created = "2026-09-19"
updated = "2026-09-20"

contract = "Separate attachment, observation and assessment; keep original tested inputs and evaluate the required result without implicit evidence writes."

[relations]
specifies = ["REQ-KIS-010"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-20T06:27:29Z"
decided_by = "technical-owner"
reason = "On 2026-09-20 the owner approved the presented recovery artifact package with \"i approve\". Record approval of this reviewed artifact in the named owner role. Reviewed full-byte SHA-256: cdf8718e6ae82aac39cd9793865a8ff1b562645b958968ddb211e8e7c3f64e42. DEC-KIS-001 separately records the explicit owner-review choice. WO approval grants the bounded execution operations in DR-015; this transition records no implementation result, assurance acceptance or external action."
+++

# Keep evidence outcomes truthful

## Scope

Separate attachment, observation and assessment; keep original tested inputs and evaluate the required result without implicit evidence writes.
This is the prospective contract for WO-KIS-010; creation does not change installed behavior.

## Rules

**KIS-EVD-001.** An attachment proves only that material is available. For each check required by the selected verification contract, distinguish success, failure, not run, unavailable and not applicable. Missing or unassessed required evidence never satisfies a successful-check condition. Not applicable needs a reason from the contract, not a missing result.

**KIS-EVD-002.** Reuse the existing explicit capture route to retain the tested candidate or working-input identity, command arguments, checker identity, exit result and output reference. Preserve useful failure output. A local record remains a local assertion; neither a hash nor a supplied actor name proves independent observation. Manual inspection or analysis remains valid when the verification contract calls for it and the responsible reviewer records its conclusion.

**KIS-EVD-003.** Readiness and scope checks must not rebind evidence, rewrite its observed candidate or create retained packets implicitly. Explicit evidence capture may write and must report its writes. Relabelling an attachment cannot change a failed, missing or stale test into a successful current run.

**KIS-EVD-004.** Reuse unchanged evidence only when the relevant candidate contents and governing inputs are demonstrably unchanged, using the existing comparison and explicit refresh route. Keep the original observation and its tested version. A successor record may reference it and explain reuse. Changed or unknown relevant inputs require fresh affected checks. Unrelated notes do not invalidate otherwise matching evidence.

**KIS-EVD-005.** The existing structured result and human summary must distinguish projection, readiness evaluation and mutation; identify checks actually evaluated, observed evidence origin, unresolved authority and writes performed. Reuse existing fields where adequate. A projection cannot be described as readiness or approval. Retain compatible readers and stable command argument boundaries.

**KIS-EVD-006.** Define required checks in the existing verification contract. Successful execution of an irrelevant command is insufficient. Preserve concise evidence references and original historical VREC/RLS facts; do not introduce a receipt service, exact prose validator, automatic equivalence engine or mandatory report header.

## Coverage

| Requirement | Rules |
| --- | --- |
| `REQ-KIS-010` | KIS-EVD-001, KIS-EVD-002, KIS-EVD-003, KIS-EVD-004, KIS-EVD-005, KIS-EVD-006 |

## Examples and failure behavior

- **Normal:** A required command ran successfully for the selected inputs. Its result remains usable when only an unrelated note changes, with its original tested version preserved.
- **Failure:** A report says required tests did not run. A handoff refuses the required successful-test claim and leaves that report unchanged.

Refusal names the failed criterion or missing input and does not imply an applied state change.
Use an existing diagnostic when its meaning fits; do not reserve new codes in this draft.

## Compatibility and KISS review

This prospectively tightens KIS-CUT-007/008/024/031 in SPEC-KIS-001: flexible attachment formats and safe reuse remain, but presence and refreshed labels never prove test success. It removes implicit handoff packet writes described by the current check guide. Existing released behavior remains governing until normal release and explicit adoption.

Reuse existing components and remove obsolete tests and instructions with the behavior
they described. No new artifact type, approval service, runtime mode or score is required.
These are repairs within the existing component responsibilities: no new architecture
is introduced and no active architecture addresses this new requirement. If implementation
reveals a material structural or trust-boundary change, obtain a bounded architecture
decision before that change rather than silently expanding this repair.
