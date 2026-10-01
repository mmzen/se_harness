+++
id = "DEC-IAR-004"
type = "decision"
title = "Sequence independent verification for the minimal layout"
status = "decided"
owners = ["mmzen"]
created = "2026-09-30"
updated = "2026-09-30"
kind = "question"
question = "Should a separately governed compatibility release on the 0.20 maintenance line precede integration of the minimal-layout candidate?"
raised_by = "Codex"
recommendation = "compatibility-release"

[[options]]
id = "compatibility-release"
label = "Prepare a compatibility maintenance release, then separately adopt it and requalify the minimal-layout candidate."

[[options]]
id = "defer-integration"
label = "Retain the tested minimal-layout work and defer its integration until a compatible released verifier is available."

[relations]
concerns = ["REQ-IAR-031", "SPEC-IAR-016", "VER-IAR-022", "WO-IAR-030"]
blocks = ["WO-IAR-030"]

[disposition]
option = "compatibility-release"
label = "Prepare a compatibility maintenance release, then separately adopt it and requalify the minimal-layout candidate."
decided_by = "mmzen"
decided_at = "2026-09-30T19:31:48Z"
reason = "Human mmzen selected: Prepare compatibility release (Recommended). Prepare a compatibility maintenance release on the 0.20 line, then separately adopt it and requalify the minimal-layout candidate. This selects the plan and authorizes artifact preparation only; implementation, verification acceptance, release, publication, adoption, push and PR decisions remain separate. Codex applies the recorded human decision."

[[lifecycle_events]]
from = "open"
to = "decided"
decided_at = "2026-09-30T19:31:48Z"
decided_by = "mmzen"
reason = "Human mmzen selected: Prepare compatibility release (Recommended). Prepare a compatibility maintenance release on the 0.20 line, then separately adopt it and requalify the minimal-layout candidate. This selects the plan and authorizes artifact preparation only; implementation, verification acceptance, release, publication, adoption, push and PR decisions remain separate. Codex applies the recorded human decision."
+++

# Sequence independent verification for the minimal layout

## Observed dependency

The repository and CI select released 0.20.0. Its candidate acceptance runner
unconditionally reads customized/ENGINEERING_HARNESS.md. The accepted minimal
layout deliberately creates no such file. Against the exact candidate wheel
below, the released runner raises FileNotFoundError before completing qualification.
The candidate runner handles both layouts and passes its scenarios, but candidate
code cannot supply the independent released-verifier authority required by CI.

- Candidate commit: 6dd70f29cd43ffc230779d61ee1a7ced43a7a611.
- Candidate wheel SHA256: e518c10d0fe34ae8d2864d7af5ecef0f84e0b94fe4c90afccc4f2d407b791f3b.
- Evidence: ../evidence/WO-IAR-030/compatibility-check.json.
- Current CI selection: .github/workflows/candidate-evidence.yml derives the
  exact public predecessor and invokes its qualify candidate-package operation.

This question concerns the delivery sequence. It blocks further WO-IAR-030
transitions until the sequence is decided; completed local implementation and
observed tests remain retained. Existing CI and release checks remain required.
No CI job has been run for this local branch yet; the failure above is a local
reproduction using the same released acceptance runner.

## Options

**compatibility-release (recommended).** Prepare a bounded maintenance package
from the authorized 0.20 release line. Backport only the acceptance-runner behavior
needed to assess both retained repository-copy layouts and the successor external
layout. Preserve the maintenance release's existing init behavior, scenario IDs,
identity checks, gates and independent-verifier contract. Publish that maintenance
release through the existing procedure. Separately adopt its exact identity for
the root/CI selection, then requalify this successor candidate. This adds one
release/adoption cycle but keeps the independence rule and minimal default intact.

**defer-integration.** Keep the tested implementation on its local branch and wait
for a compatible released verifier. This avoids a maintenance release now but
delays integration and the requested successor release. It does not authorize
skipping qualification or restoring instruction copies to satisfy the old test.

## Proposed implementation sequence

1. Prepare the bounded maintenance work order, verification contract and release
   inputs from the existing 0.20 maintenance baseline. Select the next available
   maintenance version during that preparation; no version is allocated here.
2. Reuse the corrected acceptance scenarios: identify the layout explicitly,
   assert the two-file default for the successor, and select a Git integration
   for the managed-content refusal. Reject unsupported layouts. Do not copy the
   new installer or resource system into the maintenance product.
3. Verify the maintenance candidate on Windows and Linux. Test its unchanged
   legacy initialization, its ability to assess the exact minimal wheel, and all
   existing refusal scenarios. Use released 0.20.0 to qualify the maintenance
   candidate, whose default footprint remains compatible with that verifier.
4. Complete the existing release and delivery procedure, including the declared
   marketplace, documentation, observation and marker obligations. Human assurance,
   release and publication decisions remain separate.
5. Prepare a separate adoption work order for the exact published maintenance
   evaluator. Review the root/CI identity changes under that authority.
6. Reconcile this branch with the adopted baseline. Rebuild and requalify its exact
   successor candidate with the compatible released verifier, finish the remaining
   integrated/native assessment and prepare VREC-IAR-020. Preserve desktop delivery
   as unverified until actual evidence exists; CLI results do not supply it.

## Decision boundary

Choosing compatibility-release authorizes preparation of its artifact package.
It does not itself approve implementation, publication, adoption, verification
acceptance, push or PR creation. The current work orders do not cover those changes.
The installed evaluator remains 0.20.0 until the separate adoption is authorized
and applied. DEC-IAR-003's future-release and separate-adoption boundary remains.

## Disposition

Pending the human decision; apply it through the selected released evaluator.
