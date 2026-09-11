+++
id = "WO-RLO-009"
type = "work_order"
title = "Exclude retained evidence from release artifact discovery"
status = "in_progress"
owners = ["engineering-owner"]
created = "2026-09-11"
updated = "2026-09-11"

[assurance]
commit_bound_verification = "required"
rationale = "Publication relies on the resolver selecting real governed artifacts and preserving their exact release identities. The changed executable discovery behavior requires commit-bound assurance."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  ".github/scripts/publish_dashboard.py",
  ".github/scripts/publish_release.py",
  "tests/test_dashboard_publication.py",
  "tests/test_release_orchestration.py",
  "tests/test_ci_pipeline.py",
  "tests/test_artifact_authoring.py",
  "docs/engineering/release-orchestration/work-orders/WO-RLO-009.md",
  "docs/engineering/release-orchestration/verification/VER-RLO-006.md",
  "docs/engineering/release-orchestration/evidence/WO-RLO-009/",
  "docs/engineering/release-orchestration/verification-records/VREC-RLO-009.md",
  "docs/engineering/release-orchestration/evidence/VREC-RLO-009-evaluator.json",
]

[relations]
implements = ["REQ-RLO-001"]
specifications = ["SPEC-RLO-001"]
architecture = ["ARCH-RLO-001", "ADR-RLO-001"]
verification = ["VER-RLO-006"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-11T12:57:17Z"
decided_by = "engineering-owner"
reason = "The operator stated on 2026-09-11: I approve both artifacts and authorize implementation. This records engineering-owner approval of the bounded repair and required commit-bound verification classification reviewed in PR 452 at 553c7badf6f742c092b0b2d284f95e2e4ca60428. Start remains subject to preflight; completion, VREC preparation, assurance and merge remain separate decisions."

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-09-11T12:58:44Z"
decided_by = "engineering-owner"
reason = "The operator explicitly authorized implementation with approval of both artifacts on 2026-09-11. Released evaluator 0.17.0 start preflight passes for the approved packet and its governing reading manifest has been read. Start only the declared discovery repair; no completion, preparation, assurance or merge decision."
+++

# Work Order: Exclude retained evidence from release artifact discovery

## Lifecycle

The operator approved this WO and VER-RLO-006 and authorized implementation on
2026-09-11. The lifecycle events record approval and start through the released
evaluator after passing start preflight. No execution delegation is granted.
Completion, VREC preparation, assurance and merge remain separate decisions.

## Approved scope extension — 2026-09-11

The operator stated "i accept the extension", accepting the
[reviewed proposal](../evidence/WO-RLO-009/scope-extension-proposal.md) at
`a53f5663bb812aa0c91d9f01ad2d104311d20fc9`. The
[approval receipt](../evidence/WO-RLO-009/extension-approval.json) records the
engineering-owner and assurance-owner decisions and reviewed file digests.

The added scope is confined to the named allocation test in
`tests/test_artifact_authoring.py`: rename its temporary `.git` directory
instead of deleting read-only Git objects, and remove the unused local import.
Every assertion and product implementation stays unchanged. VER-RLO-006 DISC08
requires the corrected case and both full platform suites to pass.
Existing discovery scope and authority boundaries remain unchanged.

## Objective

Restore release resolution when engineering evidence contains copied artifact
front matter, without weakening rejection of ambiguous live artifacts.

## In scope

Baseline: `fb6f60d5069706e8ae0ca69d1263285cbb904f45`, the merge of PR #451.
The [incident observation](../evidence/WO-RLO-009/incident.json) records the
failure and the comparison with the preceding main revision.

1. Apply the validator's existing directory-exclusion semantics before parsing
   Markdown in the publication helpers. Match directory segments below
   `docs/engineering`, not substrings or artifact-ID prefixes.
2. Cover the complete-tree catalog, release-record search, and changed-path
   search used to find the first integration of a released record. Check the
   rehearsal selector, which also uses these helpers.
3. Keep explicit reads of bound evidence available. Exclusion from artifact
   discovery must not exclude evaluator sidecars or other evidence from use.
4. Add regression cases to the existing test files and retain their results.

This restores SPEC-RLO-001 rules 3–5: trusted-main resolution, unique formal
identity, and consistent release provenance. It introduces no new product rule.

## Out of scope

Changes to the portable validator, managed files, CI definitions, archive limits,
release schemas, plugin behavior, existing artifacts, or retained evidence.
No cleanup of historical fixture IDs. No live release, tag, deployment or merge.

## Authorized decision envelope

After approval and start, the implementer may choose the path predicate's name,
local factoring and disposable Git fixtures within the listed files. All
discovery callers must use consistent rules. Existing trust boundaries and
duplicate-ID errors remain in force. Completion and VREC preparation retain
their separate accountable decisions; VREC-RLO-009 is reserved, not prepared.

## Constraints

Read paths and metadata from the selected Git revision. Do not use current
working-tree contents or import code from an untrusted candidate checkout.
Check parity with the canonical validator's exclusion semantics; leave that
validator unchanged. Preserve the bytes and modes of every pre-existing
engineering artifact and evidence file.

The baseline archive has 9,983 entries against the existing 10,000-entry limit.
Use existing test files and a small number of evidence bundles. Stop if the
completed candidate or later governance commits exceed that limit.

## Expected change surface

Repository publication discovery helpers, their existing regression suites,
this two-artifact packet and its own evidence. No consumer installation change.

## Required verification

Pass VER-RLO-006 cases DISC01–DISC07 on Windows and Linux, using released
SE Harness 0.17.0 for governing checks. Prove the original failure first and
successful resolution afterward on the same frozen trusted-main tree.
Also pass DISC08 for the approved fixture-only correction on both platforms.

## Evidence to record

Retain exact commands, runtimes, candidate and trusted-main commits, expected
and observed outcomes, unchanged-history comparison, archive count, and hosted
check identities under `evidence/WO-RLO-009/`. Summaries reference raw results.

## Stop and escalate conditions

Stop on failed gates, changed scope or discovery semantics, modified historical
bytes, a remaining true duplicate, a failed preservation check, or missing
platform evidence. Do not relabel a failed check as a transient retry.

## Completion report format

Use the selected harness result. State the changed discovery behavior, test
results, exact candidate, retained evidence, remaining blockers and one next
accountable action. Distinguish implementation from assurance and merge.
