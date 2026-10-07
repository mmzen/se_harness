+++
id = "SPEC-HAG-007"
type = "specification"
title = "Private test-copy lifecycle and export contract"
status = "approved"
owners = ["mmzen"]
created = "2026-10-06"
updated = "2026-10-06"
contract = "Rehearse released-evaluator lifecycle operations atomically in an explicit test copy, and export exact records with ordinary Git provenance while real Git authority remains unchanged."

[relations]
specifies = ["REQ-HAG-011", "REQ-HAG-012", "REQ-HAG-013"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-06T18:40:36Z"
decided_by = "mmzen"
reason = "Human mmzen answered \"I approve\" to the Phase 3 package published in PR #542 at 689dee3b1929e5c58338df1331a0eb9df484ce25. Approves the nine governing definitions and WO-HAG-008, including required commit-bound verification under VER-HAG-006 and its bounded local execution. Git remains authoritative; this is a private test-copy lifecycle rehearsal. Authentication and database ACL implementation remain deferred; existing controls stay. Includes the reviewed bounded publication grant to mmzen/se_harness, source codex/hosted-artifact-phase3, target main, draft PR #542, including the ready record and a later separately supplied verification-decision push. No risk acceptance, actual assurance decision, merge, real authority cutover, release, deployment or host-plugin update is granted."
+++

# Private test-copy lifecycle and export contract

## In plain words

Exercise the complete workflow in a disposable graph project. Keep Git
authoritative for real work. Use the existing released evaluator for every
lifecycle answer and every generated record.

## Scope and terms

This contract adds lifecycle rehearsal and export to the delivered Phase 2
sandbox. DEC-HAG-004 selects its boundary; accepted Phase 2 definitions remain
unchanged. Authentication and graph ACL implementation remain deferred.

- **Test project:** An explicitly marked disposable project containing immutable
  imported history and newly authored rehearsal records.
- **B:** An immutable hosted input baseline, including artifact and evidence bytes.
- **S:** The Git commit from which the test's source fixture was obtained.
- **P:** A real Git commit containing a materialization of B and its test source
  in a disposable repository. P is a test candidate, not a real product candidate.
- **C:** The actual implementation commit assessed for this work order in Git.
- **Complete result:** Every permitted artifact and evidence file changed by one
  released command, plus its operation receipt and resulting graph heads.

## Rules

### HAG-PILOT-001 — Explicit rehearsal boundary

Lifecycle operations MUST require a project marked as a test copy and an explicit
test-copy selection in the client request. Responses, receipts, exported manifests
and walkthrough output MUST identify this boundary. Supplied decision actors are
test inputs; they MUST NOT be presented as authenticated human consent.

Imported real artifact revisions MUST remain immutable. Lifecycle changes apply
only to newly authored rehearsal records in that project. The service MUST NOT
write real checkout artifacts, rewrite imported approvals or invoke external
publication, tagging, marketplace or deployment actions. A test RLS in `released`
state has no external effect. Keep the existing private listener, credential,
principal, path-containment and constrained-Cypher controls. Keep Cypher available.

### HAG-PILOT-002 — Closed evaluator operations

Use the separately installed released evaluator 0.22.1 with the wheel/payload
identities already pinned by SPEC-HAG-003 and the Phase 2 manifest. Its actual
identity MUST be checked and retained. The service MUST NOT compute a parallel
lifecycle, weaken a gate, patch generated record bytes or run candidate source
as its evaluator.

Extend the remote contract with typed inputs for these operation families:

| Family | Released operation | Effect |
| --- | --- | --- |
| Inspect readiness | `check`, `preflight`, `validate` | Read results; checkpoint-free checks grant no authority |
| Preview selected state changes | `transition` without `--apply` | Retained preview; no graph mutation |
| Apply selected state changes | `transition --apply` | Complete permitted changes after fresh evaluator checks |
| Record test decision | `decide`, including its supported disposition options | Exact evaluator-produced decision and any related changes |
| Record test risk | `raise-risk`, with optional evaluator-supported paired decision | Complete generated record set |
| Retain handoff | `check --checkpoint handoff` | Evidence-producing operation, committed with its sidecars |
| Prepare test verification | `capture-verification` | Unmodified VREC and evaluator evidence |
| Prepare test release | `prepare-release` | Unmodified RLS and evaluator evidence |

Existing import, draft authoring, freeze, reads and seven read-only MCP tools
remain supported. Add no general shell, arbitrary command forwarding, user-chosen
executable or evaluator `--test-command` execution endpoint. The approved local
qualification runner produces test evidence; the service receives bounded bytes
and hashes. Define the exact request/result schemas and permitted file effects
before implementation, using the installed command help and canonical fixtures.
Unsupported options and unsupported lifecycle edges fail explicitly.

### HAG-PILOT-003 — Complete atomic writes

For each mutation, materialize an isolated input projection, run the released
command and compare all files before and after. Admit only outputs allowed for
that typed operation. Store exact artifact bytes and opaque evidence-file bytes;
an unrecognized output or missing required sidecar rejects the whole operation.

Commit all revisions, file digests, selected heads, project/context versions and
the operation receipt in one Memgraph transaction. No partial result may become
visible. Preserve historical revisions. A command failure or transaction failure
leaves the prior selected state intact and returns the actual failure.

### HAG-PILOT-004 — Guarded preview, apply and retry

Bind preview and apply to the selected project, complete input snapshot, context
and artifact versions, command inputs and evaluator identity. Reject apply if
any bound input changed; rerun the evaluator's required checks before committing.

Retain the existing principal-scoped idempotency semantics. Identical retries
return the same receipt and byte hashes; a changed request under the same key
fails. Two writes based on the same incompatible expected versions cannot both
commit. A lost reply is an unknown outcome until receipt lookup resolves it;
restart MUST preserve the receipt and its associated complete result. Temporary
Git projections are staging, not an independent accepted state.

### HAG-PILOT-005 — Ordinary Git provenance for test records

Verification capture MUST run against clean ordinary Git history in the disposable
test repository. Commit P contains the exact selected input bytes of B and source
fixture S. Retain a manifest of B, S, P, their file hashes and evaluator identity.
P excludes the VREC that will be generated from it. Later governance commits may
add records, but their existence MUST NOT change the candidate bound in that VREC.

Use the released capture and release-preparation commands without altering their
candidate or provenance fields. Retain all referenced Git objects needed by
subsequent checks. The manifest MUST distinguish P from actual implementation
candidate C. No claim of new native hosted C+B assurance is made by this pilot.

If 0.22.1 cannot faithfully perform a required operation on this ordinary test
projection, report the exact failed contract and stop that operation. Any new
evaluator change, release, adoption or accepted-definition amendment requires
its own reviewed scope; do not substitute a candidate governor.

### HAG-PILOT-006 — Exact export and replay

Export a selected immutable snapshot with its artifact/evidence paths, exact
bytes, digests, provenance manifest and a self-contained Git bundle containing
the required test history. Check missing objects and hashes before reporting
success. Label the export as test data. Retain selected history and relationships;
do not silently export current heads when an older snapshot was requested.

The client writes only to an explicitly supplied new destination. Refuse existing
destinations, unsafe paths, links, corrupt bytes and missing dependencies. Partial
downloads remain identified as incomplete. An independent clean replay checks the
same selected state, links and candidate bindings with released 0.22.1. Comparing
semantic results may exclude only enumerated incidental timestamps and temporary
absolute paths; exported artifact/evidence bytes themselves must match exactly.

### HAG-PILOT-007 — Bounded compatibility and operation

Version the added mutation/result contract separately from Phase 2 v1. Publish
closed schemas with examples and refuse unknown schema versions. Existing v1
requests retain their behavior; they cannot invoke the new lifecycle operations.
Use a separate disposable project and data volume for the pilot. This work does
not promise migration of existing Phase 2 volumes.

Retain one service, one database and synchronous requests. Bound requests,
responses, projection concurrency and subprocess time through explicit settings;
existing defaults remain unless measured pilot evidence justifies a documented
bounded adjustment. Report oversize/timeout failures without partial graph writes.
Do not add a background queue, workflow engine or production authorization system.

### HAG-PILOT-008 — Qualification and walkthrough

The packaged walkthrough MUST use an installed client and packaged service to
create a test change, accept its definitions, start and complete test work,
prepare and assess a test VREC, prepare and assess a test RLS, reconcile a lost
reply, export, and independently replay. Run with a real Memgraph engine.

VER-HAG-006 defines required boundary, concurrency, restart and failure cases.
Retain actual component identities, commands, exits, failures and omissions.
Mocked results do not establish hosted qualification. Codex/Claude live sessions,
desktop, startup and compaction delivery are outside this contract; do not infer
them from packaged CLI or MCP tests.

## Failure behavior

| Trigger | Required result |
| --- | --- |
| Missing test selection or imported record mutation | Explicit boundary refusal; no writes |
| Evaluator refusal or unsupported command | Preserve evaluator reason; no committed result |
| Stale preview/version or conflicting idempotency input | Conflict; retrieve current state or existing receipt |
| Failure after staging any output | Whole graph transaction rolls back |
| Lost reply after commit | Unknown response; receipt reconciliation returns original result |
| Missing/corrupt provenance, file or Git object | Capture/export/replay fails; never relabel a candidate |

Wire error names are selected in the closed schema before implementation. Preserve
the distinction between refusal, conflict, evaluator failure and unknown outcome.

## Examples

Given a clean test candidate P, capture creates a VREC and sidecar with their exact
released bytes. A fault before graph commit exposes neither. A lost reply after
commit is recovered with the original receipt (HAG-PILOT-003 through 005).

Given an exported older baseline, replay reconstructs its files rather than the
newest graph heads and resolves the original P (HAG-PILOT-006).

## Coverage

| Requirement | Rules |
| --- | --- |
| `REQ-HAG-011` | HAG-PILOT-001, HAG-PILOT-002, HAG-PILOT-007, HAG-PILOT-008 |
| `REQ-HAG-012` | HAG-PILOT-003, HAG-PILOT-004, HAG-PILOT-007 |
| `REQ-HAG-013` | HAG-PILOT-005, HAG-PILOT-006, HAG-PILOT-008 |

## Implementation choices

Wire field names, internal module layout and concrete test-fixture content remain
implementation choices. They must satisfy this contract and preserve existing
Phase 2 behavior. ADR-HAG-003 records the proposed projection design.
