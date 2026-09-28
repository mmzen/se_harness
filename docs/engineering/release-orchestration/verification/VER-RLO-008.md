+++
id = "VER-RLO-008"
type = "verification"
title = "Release delivery completion and handoff verification"
status = "approved"
owners = ["mmzen"]
created = "2026-09-28"
updated = "2026-09-28"

[relations]
verifies = ["REQ-RLO-018", "REQ-RLO-019", "REQ-RLO-020"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-28T19:38:37Z"
decided_by = "quality-owner"
reason = "Human repository owner mmzen: \"I approve\", responding to the seven-artifact release-delivery package and required commit-bound verification request on 2026-09-28. Reviewed SHA-256 120acb98ef1615017295693cc0aaef6705fbf1f8821a04b5fda270916701ffde; transition input SHA-256 120acb98ef1615017295693cc0aaef6705fbf1f8821a04b5fda270916701ffde. Legacy evaluator role quality-owner records the human decision; Codex applies it. Only the confirmed assurance fields and confirmation text were added to WO-RLO-011. Implementation is bounded by that work order; no external action is authorized."
+++

# Verification Contract: Release delivery completion and handoff verification

## Independence

Derive expected outcomes from REQ-RLO-018 through REQ-RLO-020 and
SPEC-RLO-006. Define fixtures before inspecting candidate output. Tests use
synthetic package identities and retained evidence; they must not label them as
actual publication observations. Human verification acceptance is separate from
the implementing agent's evidence collection.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
|---|---|---|---|
| REQ-RLO-018 | test, inspection | DLV-01, DLV-02, DLV-07 | Every surface is represented; omissions fail; pending post-publication work has an owner and next action. |
| REQ-RLO-019 | test, inspection | DLV-03, DLV-04, DLV-05, DLV-07 | Mismatched identities, local-only proof, stale or absent evidence and wrong public routes cannot satisfy closeout. |
| REQ-RLO-020 | test, inspection | DLV-01, DLV-02, DLV-06, DLV-07 | Only complete evidence passes; deferrals stay outstanding; no lifecycle or external mutation is added. |

## Acceptance scenarios

| Case | Inputs and action | Expected result |
| --- | --- | --- |
| DLV-01 | Complete plan with all five surfaces, matching evidence, observed released RLS, and no deferral; include one justified unchanged surface. Run the reporting command. | Exit zero; overall complete; formal state and evaluator publication remain separate fields. Remove the unchanged justification and rerun. It must not pass. |
| DLV-02 | Published evaluator 0.19.0 and released RLS; marketplace expected to advance from 0.1.0 but still pending. Also exercise omission and explicit deferral. | Never complete. Pending/deferred cases show the owner and next action; omitted surface is invalid. Evaluator success remains visible. |
| DLV-03 | Same plugin version with different installed-content digest, wrong bundled evaluator, wrong public commit or wrong observation-to-plan binding. | Each materially different identity fails with the conflicting values identified; agreement between two stale documents cannot satisfy the expected identity. |
| DLV-04 | Local qualification only; then public fresh-install proof without update proof for one claimed host; then both routes with correct public identity. | First two remain incomplete; only the third supplies sufficient marketplace observations. Another local path or public destination is not accepted as equivalent. |
| DLV-05 | Missing/unreadable evidence, wrong evidence digest, duplicate JSON key or surface, unknown schema, and a path escaping the evidence root. | Nonzero result with a bounded diagnostic; no apparent completion. Exercise a symlink escape where the test host supports it; report an unsupported case explicitly. |
| DLV-06 | Run complete and incomplete reports against disposable inputs; compare repository and input bytes before/after. Inspect imports and subprocess/network usage. | No file, lifecycle, credential, network or public-state mutation; no execution of input strings. Exit codes distinguish incomplete from invalid input. |
| DLV-07 | Inspect the updated release sequence and publication handoff. Execute the documented synthetic example. Inspect the full candidate diff. | Commands match the implemented interface; outputs and responsible actors are explicit; evaluator publication precedes dependent assembly; human publication rights and all scope limits remain intact. |

## Execution environment and commands

- Govern the work with the repository-selected released evaluator 0.19.0 from
  its absolute private Python path, outside the checkout, using `-I -m se_harness`.
- Run the new focused suite on the available Windows host with Python 3.14:
  `python -m unittest discover -s tests -p "test_release_delivery.py"`.
- Run the repository's existing release-orchestration and publication-related
  regression suites selected from the current test layout. Retain the exact
  commands and collection counts; do not invent names or claim unrun tests.
- Run artifact validation and the selected work's required scope, handoff and
  transition checks. Retain their actual results.
- The focused tests must use local temporary evidence and no live host login,
  marketplace update or publication. Hosted CI supplies additional platform
  evidence only when it actually runs.

## Manual assessment

The reviewer confirms that one read-only script and the guide changes satisfy
the agreed prevention outcome. Review the minimum observations against the
actual public-marketplace failure. Confirm that the command's supplied-evidence
limit is visible and that the portable harness and publisher boundaries remain
unchanged. Link each finding and its resolution in the retained review.

## Evidence retention

Retain commands, exit codes, focused and regression test outputs, the documented
example outputs, inspection findings, limitations and requirement assessment in
the selected work order's evidence directory. Bind the final verification record
to one exact clean candidate commit through the released capture procedure.
Include this contract and every selected work order in that record.

## Residual uncertainty

This verification establishes the new procedure and local reporting behavior.
It does not establish that a new plugin has been published or installed from the
public branch. Subsequent marketplace work must supply real fresh/update and
native instruction-delivery evidence for its exact selected package. It also
does not retroactively change historical release acceptance.
