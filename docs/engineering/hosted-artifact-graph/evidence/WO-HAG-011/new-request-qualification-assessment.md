# New-request qualification assessment

Candidate: `946d566b1f3f79cfdf5060242ba39fde045c1774`.
Contract: activated `VER-HAG-008 EFF-04A2`; selected work: `WO-HAG-011`.

**Result: failed content review.** Claude saved a mechanically valid intent but
invented required meaning and reported complete content. Further native tests
stopped under the approved first-Claude failure rule. No work completion or
verification is claimed.

## Decision applied

mmzen approved the [exact linked revision](diagnostic-review-20261010/review.md)
and bounded manual activation. The [activation record](diagnostic-review-20261010/activation.json)
binds the actual response and exact accepted/revised bytes for SPEC-HAG-008,
VER-HAG-008 and WO-HAG-011. Definitions stay approved; work stays in progress.
Historical copies, lifecycle metadata and earlier results remain unchanged.

The guide identifies the hosted command route and the tool reference states
that remote creation has no local `--dry-run` preview. The new request asks to
adapt the greeting for a new audience. The unused `diagnostic_scope` selection
field was removed: its case classification and expected answer are assessor-only.
Original fixture bytes, model and permissions are unchanged.

## Observed result

Claude acknowledged the existing English greeting, imported the seven records,
and saved only `INT-P3-001` as a draft. It claimed that the new audience needs
to be addressed directly, treated an adapted return value plus manual inspection
as the success measure, and invented exclusions such as keeping the original
behavior and excluding internationalisation. The request does not establish
those choices or the agreed operational outcome and measure.

Its report marks every intent checklist item complete and says no unsupported
constraints were added. The final reply also calls the draft complete. This fails
the required incomplete-draft or exact-blocker behavior. The evaluator's shape
validation passes; it does not assess the missing meaning.

The [independent assessment](claude-151-assessment.json) identifies each finding.
The [visible transcript](claude-151-visible.md), [evidence archive](claude-151-evidence.zip)
and [inventory](claude-151-inventory.json) retain inputs, saved document, report,
commands, readback and identities. Private reasoning and credentials are omitted.

## What passed

- Both packaged plugins match committed guidance. Nine canonical instruction
  sections and all 12 fixture files match their sources exactly.
- The agent input contains the exact approved request and no negative-case label.
- An independent service read matches the submitted document byte for byte.
- All seven imported records still match their original Git-blob bytes.
- Staged inputs are unchanged; no lifecycle decision or fixture change occurred.
- No native call failed or was denied. Claude used the observations command;
  its zero-failure report agrees with captured events. The unsupported remote
  `--dry-run` call did not recur in this one trial.

Correct mechanics and reporting do not establish reliable semantic review or
repair historical failures.

## Cost and scope

| Measurement | Observed |
| --- | ---: |
| Claude wall time | 226.201 seconds |
| Native calls | 13: 4 Read, 7 Bash, 2 Write |
| Model turns | 11 |
| Initial input context | 32,677 tokens |
| Peak input context | 58,356 tokens |
| Delivered task | 62,179 bytes |
| Captured client execution time | 7.273485 seconds |
| Exact builds, package preparation and client install | 390.812 seconds |

This negative diagnostic is not successful positive authoring. The positive goals
remain below 180 seconds, at most 15 calls and below 40,000 peak input tokens.
This trial meets only the call threshold. EFF-04B is unperformed. Provider time
is unclassified. No same-task speed claim is made against historical EFF-04A.

The entry contains 21,262 canonical-instruction bytes, 18,177 selected-reference
bytes, 5,490 fixture bytes, 13,148 selection/provenance bytes and 4,102 other task
bytes. The guide/reference edit removes only 633 bytes. The instruction load
remains large for one artifact, with required content review still failing.

## Supporting evidence

Two pinned builds produced identical wheel and sdist bytes.
Wheel SHA-256: `05286a54ea8fd16e621cfd4cfdf997838d340a6f2fe40f23c4f5aa8c8780de37`.
Sdist SHA-256: `93f3c36cc1a6f074a4530b15969a810ad75d9b9ee1ee9ba0d9409de8e2a16e39`.
The separate candidate client is 0.22.2; governor is released 0.22.1; packaged
plugin is 0.2.7. The current host installation is unchanged. Claude used
`claude-opus-4-6` with retained normal permissions and a passing live auth probe.
[candidate21-checks.zip](candidate21-checks.zip) contains exact commands and identities.

All 127 wheel member payloads match candidate15. EFF-02/03 runtime checks are reused
only for those identical bytes, not for changed instructions or the new task.
The preparation source suite (1,336 tests, 24 skips), plugin, distribution and smoke
checks are reused because their source/test/build/guide bytes did not change during
activation. [Activation checks](diagnostic-review-20261010/activation-checks.json)
record that boundary. Fresh released validation finds 1,991 artifacts, zero errors
and 63 existing warnings; scope and review preflight pass.

## Review and next boundary

This trial shows that the agent received the applicable instructions and original
facts but substituted plausible content for missing owner input. It does not
establish that another warning or wording variation would correct that behavior.

The command clarification adds no code, dependency or orchestration layer. Calls
serve selection, import, draft creation/submission, readback and reporting.
Further simplicity work should examine the demand for a formal draft from an
underspecified request and the size of its mandatory entry. Separating clarification
from authoring is a possible proposal for review, not an activated contract change.
Further variations require review under the approved stop condition.

Codex A2 and all positive cases remain unperformed on this candidate. Full
WO-HAG-009/010 qualification is incomplete. This trial's containers are stopped;
volumes and evidence are preserved. Historical EFF-04A failures remain failures,
and this new task does not establish that the original request now works.

PR #543 stays draft against main. At pre-publication head `acfc1bc5`, source,
package, Windows/Linux upgrade/integration and CodeQL checks passed. Harness
validation failed QGP-G4I-EVIDENCE: WO-HAG-009 has no handoff evidence for the current
formal snapshot. No replacement packet was fabricated. New-head CI is reported
separately after publication.

WO-HAG-011 remains `in_progress`. The released evaluator returns
`PROC-WO-IMPLEMENT / STEP-WO-IMPLEMENT-CHECK`, with
`harnessctl check REPO --artifact WO-HAG-011 --checkpoint handoff`.
The failed content criterion prevents a completion or verification claim.
