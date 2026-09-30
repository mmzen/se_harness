+++
id = "WO-IAR-026"
type = "work_order"
title = "Remove the six adopted compatibility pointers"
status = "implemented"
owners = ["mmzen"]
created = "2026-09-30"
updated = "2026-09-30"

[assurance]
commit_bound_verification = "required"
rationale = "Human mmzen confirmed required commit-bound verification when approving WO-IAR-026 and VER-IAR-018. Later instruction-discovery and integration decisions depend on the six removed pointers and corrected catalog test."
decided_by = "mmzen"

[execution_scope]
paths = [
  "docs/engineering/OPERATING_CARD.md",
  "docs/engineering/DECISION_RIGHTS.md",
  "docs/engineering/QUALITY_GATES.md",
  "docs/engineering/WORKFLOW.md",
  "docs/engineering/TRACEABILITY.md",
  "docs/engineering/TECHNICAL_COMMUNICATION.md",
  "tests/test_artifact_catalog.py",
  ".engineering-harness.lock",
  "docs/engineering/instruction-architecture/work-orders/WO-IAR-026.md",
  "docs/engineering/instruction-architecture/verification/VER-IAR-018.md",
  "docs/engineering/instruction-architecture/verification-records/VREC-IAR-016.md",
  "docs/engineering/instruction-architecture/evidence/VREC-IAR-016-evaluator.json",
  "docs/engineering/instruction-architecture/evidence/WO-IAR-026/"
]

[relations]
implements = ["REQ-IAR-028"]
specifications = ["SPEC-IAR-015"]
verification = ["VER-IAR-018"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-30T06:17:22Z"
decided_by = "mmzen"
reason = "Human mmzen: I approve, confirming the reviewed six-file byte hashes, bounded test correction and required commit-bound verification. Native delivery and consumer checks must pass before deletion. Reviewed draft SHA-256 522bea0051eb224d4990733bdcb9e5a6eece57d304ff0c29365bac63fada3303. Only the supplied assurance classification was added before preview."
scope_paths = ["docs/engineering/OPERATING_CARD.md", "docs/engineering/DECISION_RIGHTS.md", "docs/engineering/QUALITY_GATES.md", "docs/engineering/WORKFLOW.md", "docs/engineering/TRACEABILITY.md", "docs/engineering/TECHNICAL_COMMUNICATION.md", "tests/test_artifact_catalog.py", ".engineering-harness.lock", "docs/engineering/instruction-architecture/work-orders/WO-IAR-026.md", "docs/engineering/instruction-architecture/verification/VER-IAR-018.md", "docs/engineering/instruction-architecture/verification-records/VREC-IAR-016.md", "docs/engineering/instruction-architecture/evidence/VREC-IAR-016-evaluator.json", "docs/engineering/instruction-architecture/evidence/WO-IAR-026/"]

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-09-30T06:17:55Z"
decided_by = "Codex"
reason = "Execution of DR-WO-START under recorded work-order approval; relevant local gates passed. Start under human mmzen approval of the reviewed cleanup and required assurance; consumer, native delivery and exact byte checks remain mandatory before deletion."

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-09-30T06:30:24Z"
decided_by = "Codex"
reason = "Execution of DR-WO-COMPLETE under recorded work-order approval; relevant local gates passed. Completed under mmzen approval. Exactly six reviewed stock pointers removed; catalog test corrected. All other pre-existing tracked files retain exact bytes. Both actual-profile hosts pass native startup and manual compaction before and after cleanup. Full suite: 1162 tests, 17 skips; affected suite: 67 tests. Released reconciliation, doctor, validation, review preflight and complete Git-derived handoff pass. Human verification and hosted CI remain separate."
+++

# Remove the six adopted compatibility pointers

## Objective

Remove the six obsolete guide pointers from mmzen/se_harness after adoption
of released 0.20.0. Agents must continue to discover the current instructions
without these files. Preserve owner content and supported older-release behavior.

## In scope

1. Inventory the active Codex and Claude hosts and plugins. Review their current
   routes and native startup/compaction evidence before deleting any pointer.
2. Confirm all six paths below are regular stock files with the reviewed hashes.
   Remove them only after every consumer, delivery and byte check passes.
3. Update tests/test_artifact_catalog.py: replace the current-repository test
   that requires TRACEABILITY.md with checks that the six retired pointers are
   absent and the current catalog, definition-link, work/evidence and root
   routes still resolve. Preserve the released legacy fixture test and its hashes.
4. Run the selected released installer's upgrade preview and authorized
   reconciliation, then doctor and VER-IAR-018. The lock already omits these
   seeds; no lock change is expected. Never edit the lock by hand.
5. Retain the review and evidence, record completion, and prepare VREC-IAR-016
   and its generated evaluator companion at the exact permitted paths.

## Out of scope

Changing product code, plugin packages, host settings, credentials, CI or release
versions; upgrading either host plugin; rewriting historical records or accepted
definitions; removing supported migration fixtures, renderers or adapters;
removing ARTIFACT_AUTHORING.md, WORKFLOW.json, QUALITY_GATES.json, AGENTS.md,
ENGINEERING_HARNESS.md or the current harness collection; push, PR, merge,
release and publication.

## Reviewed deletion inputs

Baseline: merged adoption commit 728c057115abd4cb7dbfe8e53ad8d9993d98b1bf.
Selected evaluator: released 0.20.0, wheel SHA-256
7bcfe788c5daaf670bcee25a235663e8210002ce79ffba7162317b1f0509a6e0,
payload SHA-256 88c26138f759af78b2d7eeed3d15f92b573ff264ea6a531b2c22dbbf1905130e.

The hashes below bind the actual Windows working-file bytes. These files use
CRLF. After LF normalization their contents match the retained public 0.19.0
fixtures and that fixture's published digests. The comparison establishes stock
content; deletion still requires an exact match to the byte hashes below.

| Repository-relative path | Exact SHA-256 before deletion |
| --- | --- |
| `docs/engineering/OPERATING_CARD.md` | `f33ec9e96702ad63f5cb816bc182398fdb58fd2a55436a29a306972692faccb7` |
| `docs/engineering/DECISION_RIGHTS.md` | `f291428b93bf7165c293964be340f18935f06c06c2f981acc593d6cebd5fd95a` |
| `docs/engineering/QUALITY_GATES.md` | `647941d3301caa0aeee58afc94415c345dfaa2072f85d37e6744fa5915e216b5` |
| `docs/engineering/WORKFLOW.md` | `d9949e28d281260bd7d7aa9538dd239ea60fb18b5b0391cda2fdbab39ad7b1b3` |
| `docs/engineering/TRACEABILITY.md` | `26e43956215d49eb74d2f56d361c76c55984b2b98c84daf995d4faf5ded64a09` |
| `docs/engineering/TECHNICAL_COMMUNICATION.md` | `e8ceafc9969e1710ecaf3fd791fb9046606765bc3a4c48eed21769c6ecc2e049` |

If checkout conversion changes only line endings, report it and obtain an
updated exact input review before deletion; do not silently replace these hashes.

## Authorized decision envelope

After human approval, Codex may start this work, run read-only host probes,
perform the specified local edits and commits, retain evidence, record completion
and prepare the commit-bound verification record through released procedures.
Approval does not accept the verification record or authorize external actions.

Required commit-bound assurance is proposed because later instruction discovery
and integration rely on the removed paths and revised test. The accountable
human must confirm this classification with work-order approval. No assurance
decision or implementation authority is recorded by this draft.

## Constraints and execution order

Apply SPEC-IAR-015 IAR-RET-002 and IAR-RET-005 through IAR-RET-007 and the
installed UPGRADE.md section "Separately authorized pointer cleanup".
Check every file and active consumer before any deletion. Resolve absolute
targets within this checkout; reject symlinks, directories and ambiguous paths.

Current preparation observations: Codex CLI 0.158.0-alpha.2.1 uses plugin
0.2.2; actual-profile app-server startup and manual compaction delivered the
0.20.0 root. Claude Code 2.1.273 currently uses plugin 0.2.0. Its top-level
skills route this release to docs/engineering/harness/; the old guide references
are in explicitly legacy branches. Review or run matching native Claude
qualification before deletion. A version number alone proves neither
compatibility nor failure. No automatic desktop-chat delivery claim is made:
the current desktop chat starts outside the repository.

Retain the accepted WO-IAR-020 qualification as prerequisite evidence and
identify its exact verification record. Compare its host, plugin and input
identities with current observations; do not treat a mismatched run as current.
If a real consumer still needs a pointer, stop the affected removal and propose
a separate correction. This work does not silently upgrade that consumer.

Use ordinary file removal, not a new deletion engine. The seven implementation
paths are the six pointers and the one catalog test. Other permitted paths are
the installer-owned lock, this package and its evidence/verification outputs.

## Required verification

Execute VER-IAR-018. Run identity, doctor, artifact validation, current route
checks, the affected catalog/installer/discovery tests, the full test runner,
distribution checks and CLI smoke check. Run the complete Git-derived work
scope and handoff checks. Prepare verification against one exact clean candidate
commit. Hosted Windows/Linux CI remains required at integration.

## Evidence to record

Store the six-path hashes and classification, selected runtime, host/plugin
inventory and native observations, reference classifications, before/after
preservation comparison, installer preview/apply results, actual check commands
and outputs, complete change set and review under evidence/WO-IAR-026/.
Keep failed attempts and limitations. Store no credentials or private reasoning.
VREC-IAR-016 and its evaluator companion are generated by capture-verification.
Check the intended record ID is unused before capture; stop on a collision.

## Stop and escalate conditions

Stop before deletion if any pointer differs, any active consumer or replacement
route is unresolved, required native delivery cannot be established, approval
is absent, or a required check fails. Stop on changes outside the exact scope,
unexpected installer changes, missing authority or an uncertain write. Inspect
actual state after interruption and resume only effects not already applied.
Do not weaken a check or remove an extra file to make the cleanup pass.

## Completion report format

Report removed paths, preserved content, actual checks, candidate commit,
evidence locations and remaining limitations. Use the evaluator's current
result for the next step. Human verification acceptance remains separate.
