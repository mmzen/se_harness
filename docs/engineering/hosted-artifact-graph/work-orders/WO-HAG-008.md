+++
id = "WO-HAG-008"
type = "work_order"
title = "Implement and qualify the private hosted lifecycle rehearsal"
status = "draft"
owners = ["mmzen"]
created = "2026-10-06"
updated = "2026-10-06"

[execution_scope]
paths = ["server/", "se_harness/remote.py", "se_harness/cli.py", "tests/hosted_artifact_graph/", "tests/test_hosted_artifact_graph.py", "tests/test_remote_client.py", "tests/test_cli_shape.py", "tests/plugin_integration/test_simple_plugin.py", "plugins/verity-plane/common/skills/setup/SKILL.md", "plugins/verity-plane/common/skills/change/SKILL.md", "plugins/verity-plane/common/skills/evidence/SKILL.md", "plugins/verity-plane/common/skills/harness-orient/SKILL.md", "plugins/verity-plane/codex/README.md", "plugins/verity-plane/claude-code/README.md", "docs/notes/hosted-artifact-graph.md", "docs/notes/harnessctl-reference.md", "docs/engineering/hosted-artifact-graph/README.md", "docs/engineering/hosted-artifact-graph/intent/INT-HAG-002.md", "docs/engineering/hosted-artifact-graph/capabilities/CAP-HAG-002.md", "docs/engineering/hosted-artifact-graph/requirements/REQ-HAG-011.md", "docs/engineering/hosted-artifact-graph/requirements/REQ-HAG-012.md", "docs/engineering/hosted-artifact-graph/requirements/REQ-HAG-013.md", "docs/engineering/hosted-artifact-graph/specifications/SPEC-HAG-007.md", "docs/engineering/hosted-artifact-graph/architecture/ARCH-HAG-003.md", "docs/engineering/hosted-artifact-graph/architecture/adr/ADR-HAG-003.md", "docs/engineering/hosted-artifact-graph/verification/VER-HAG-006.md", "docs/engineering/hosted-artifact-graph/work-orders/WO-HAG-008.md", "docs/engineering/hosted-artifact-graph/decisions/DEC-HAG-004.md", "docs/engineering/hosted-artifact-graph/evidence/WO-HAG-008/", "docs/engineering/hosted-artifact-graph/risks/RISK-HAG-002.md"]

[relations]
implements = ["REQ-HAG-011", "REQ-HAG-012", "REQ-HAG-013"]
specifications = ["SPEC-HAG-007"]
architecture = ["ARCH-HAG-003", "ADR-HAG-003"]
verification = ["VER-HAG-006"]
+++

# Implement and qualify the private hosted lifecycle rehearsal

## Objective

Deliver one complete private test-copy lifecycle pilot, from authoring to a
test release decision and independently replayable export. Git remains
authoritative for real engineering work and decisions.

## In scope

1. Fix the closed operation schemas and independent fixtures from SPEC-HAG-007
   before implementing the new handlers. Demonstrate released-command feasibility
   on an ordinary disposable Git fixture and retain any exact unsupported case.
2. Extend the existing service and store for guarded multi-artifact/evidence
   writes, preview/apply, decision/risk operations, handoff, VREC/RLS preparation,
   operation receipts and recovery. Keep the separately installed 0.22.1 governor.
3. Add ordinary disposable Git projections, retained provenance and exact export
   with independent replay. Imported real records remain immutable.
4. Extend the installed remote client and plugin guidance for explicit rehearsal
   selection and the new closed operations. Keep existing read-only MCP tools.
5. Build local non-promotable client/service/plugin qualification packages,
   run VER-HAG-006 on real Memgraph, retain evidence and prepare the actual VREC.

These are execution stages in one work order, not separate approvals. Each stage
depends on the preceding required checks. This draft does not start any stage.

## Out of scope

Real graph authority cutover or synchronization into authoritative Git; new
authentication or database ACLs; public/production access; new writable MCP
tools; a UI, workflow engine or queue; migration of existing Phase 2 volumes;
evaluator policy/source changes; public release, tag, registry, marketplace,
deployment, host-plugin update, or merge. Do not change accepted Phase 2 artifacts
or historical evidence. RISK-HAG-001 remains raised.

## Expected change surface

The following existing callers and consumers were inspected while preparing
this draft. The exact scope paths in metadata control future writes.

| Paths | Reason |
| --- | --- |
| `server/` | Existing bounded service component: protocol, adapter, transaction store, artifact/evidence persistence, export, Compose/configuration, locks, packaging and qualification scripts |
| `se_harness/remote.py`, `se_harness/cli.py` | Typed remote operation inputs, test selection, receipt recovery, export and CLI registration |
| `tests/hosted_artifact_graph/` | Existing hosted fixture/qualification component; add lifecycle, atomic-result, provenance/export and restart cases without changing original v1 fixture bytes |
| `tests/test_hosted_artifact_graph.py`, `tests/test_remote_client.py`, `tests/test_cli_shape.py` | Canonical representation regressions, transport boundary behavior and exhaustive CLI classification |
| `tests/plugin_integration/test_simple_plugin.py` | Verify the development packages contain the revised guidance for both hosts |
| `plugins/verity-plane/common/skills/setup/SKILL.md` | Explicit test-project setup and unchanged real-governor selection |
| `plugins/verity-plane/common/skills/change/SKILL.md` | Closed rehearsal operations and real-authority boundary |
| `plugins/verity-plane/common/skills/evidence/SKILL.md` | Distinguish test captures/exports from real verification decisions |
| `plugins/verity-plane/common/skills/harness-orient/SKILL.md` | Read test results with their explicit scope and limitations |
| `plugins/verity-plane/codex/README.md`, `plugins/verity-plane/claude-code/README.md` | Describe candidate rehearsal support without claiming live host delivery |
| `docs/notes/hosted-artifact-graph.md`, `docs/notes/harnessctl-reference.md` | Document closed operations, exact setup/walkthrough, recovery, export and failure handling |
| This domain's `README.md` | Discoverable draft package and later factual status/evidence links |
| New package files listed in scope | Complete the draft, record later human decisions through released commands and transport the complete review package; scope does not permit rewriting accepted definitions |
| `evidence/WO-HAG-008/` | Bounded fixture expectations, command observations, retained failures, review, qualification and completion evidence |

`repository_tools/plugin_distribution.py` already assembles shared skill content;
no assembler change is planned. Client 0.22.2 and plugin 0.2.7 are already distinct
unpublished candidates: retain those development version labels and bind each
package to its exact commit/digest. No edit to root version declarations, plugin
manifests, public-version expectation helpers, CI workflows or build-release
policy is planned. Run their applicable regression checks unchanged. The existing
documentation/onboarding tests remain consumers, not planned edits.

Future actual VREC and evaluator-sidecar destinations are unresolved until
released capture allocates them. The existing automatic scope rule for records
directly verifying this work order and their declared evaluator evidence is
expected to apply; assess the actual returned paths then. Do not preallocate a
VREC or admit its parent directories. Test VRECs/RLSs belong in fixture/evidence
data, not the real formal-record directories.

## Authorized decision envelope

Proposed approval permits the listed local implementation, bounded fixture and
test commands, private disposable containers, non-promotable package builds,
local commits, required checks, evidence and actual verification preparation.
The agent may select internal module layout, wire names and fixture details
within SPEC-HAG-007. It may not replace evaluator policy or broaden authority.

The requester already authorized publishing this proposal early to draft PR
#542 in `mmzen/se_harness`, source `codex/hosted-artifact-phase3`, target `main`.
That grant covers draft updates only. With implementation approval, propose
extending the review-publication grant to this work's exact candidate, ready
verification record and later separately supplied human verification decision
on the same branch/PR. Keep the PR draft and disclose incomplete checks.
Verification acceptance and merge remain separate human decisions.

## Proposed assurance classification

Propose `commit_bound_verification = "required"`: later decisions depend on the
correctness of the new command boundary, atomic state, provenance and export.
The human must confirm this classification with package approval. No assurance
decision or `decided_by` value is recorded in this draft.

## Constraints

Reuse released evaluator 0.22.1 from its separate environment. Preserve existing
v1 requests, historical Git blobs, candidate bindings and raised risks. Use
one service, one Memgraph store, one explicit test project and a separate volume.
Test actor inputs do not grant real decision rights. No fallback into a real
checkout is permitted. Do not count absent host authentication as successful
live testing; such host tests are outside VER-HAG-006.

## Required verification

Perform all eight VER-HAG-006 scenarios and applicable source, distribution,
installed-client, packaging and CLI checks. Run released artifact validation and
scope/handoff gates with the complete observed change set. Bind the final actual
candidate and retained evidence through released capture. Test-rehearsal records
cannot substitute for that actual implementation VREC.

## Evidence to record

Use the verification contract's `evidence/WO-HAG-008/` destination. Retain exact
commands, environments, full candidate/component identities, input/output byte
digests, failures, retries, skips and unperformed checks. Protect credentials.
Large immutable archives need durable referenced locations and hashes.

## Stop and escalate conditions

Stop the affected action for a required unsupported released command, new path,
new evaluator behavior or version, amendment of an accepted contract, requested
real authority, changed security boundary, or failed required check. Preserve
the observed failure. Continue only independent work within actual authority.

## Completion report format

Report delivered behavior, exact actual candidate, eight scenario outcomes,
repository checks, evidence locations, risks and omissions, and the evaluator's
current next step. Implementation completion does not grant human verification,
merge, release or deployment.
