+++
id = "VER-IAR-020"
type = "verification"
title = "Verify packaged resources and evaluator parity"
status = "approved"
owners = ["mmzen"]
created = "2026-09-30"
updated = "2026-09-30"

[relations]
verifies = ["REQ-IAR-029"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-30T11:12:12Z"
decided_by = "mmzen"
reason = "Human mmzen: I confirm and approve. Approves the updated external-resource package and required commit-bound verification for WO-IAR-028, WO-IAR-029 and WO-IAR-030. Clarification confirmed: Ok for this plan; short bootstrap before cloning, immediate activation of the actual checkout, per-session recovery after compaction/resume and independent parallel sessions. DEC-IAR-003 separately records future release and separate adoption. Reviewed file SHA-256 7496df6322a590c3d4ee145d97d59089d40b712b93de2672a2f74f56f254f004."
+++

# Verify packaged resources and evaluator parity

## Independence

Expected behavior comes from REQ-IAR-029, SPEC-IAR-016 and unchanged lifecycle/authority
contracts, not candidate output. Use an independently built candidate wheel outside
the checkout. Released 0.20.0 remains the governing evaluator for this work.

## Requirement-to-evidence matrix

| Requirement | Check | Pass condition |
| --- | --- | --- |
| REQ-IAR-029 | Selected resource identity | Install the candidate wheel outside the source checkout. Resolve every declared guide/template/machine input; compare its identity to the independent built-distribution manifest. No repository copy is required. |
| REQ-IAR-029 | Artifact authoring | Create representative requirement and work-order drafts from packaged templates, then validate them. No template directory, root guide or extra artifact appears. Retain the actual file diff. |
| REQ-IAR-029 | Policy and discovery parity | Replay existing representative accepted/refused lifecycle fixtures through the changed resource route. States, decisions, gate predicates and next-action arguments retain their contract meaning. Every typed step resolves a valid released guide heading. |
| REQ-IAR-029 | Refusal boundaries | Alter selected version/digest or remove a required resource; verify refusal before writes. Exercise missing resource, path escape and concurrent-selection change at the shared resolver boundary, not every caller combination. |
| REQ-IAR-029 | CLI and CI independence | Run the same candidate wheel in Windows and Linux without an installed host plugin and with network disabled after setup. No candidate source fallback or workstation path enters portable records. |

## Procedure and platforms

Use Windows and Linux for portable evaluator/install checks. Use actual supported
Codex and Claude Code sessions where native support is claimed, with temporary
test repositories and existing authorized test authentication. Do not alter real
credentials or saved user settings. An unavailable host is an unassessed criterion,
not a passing mock or permission to omit its required qualification.

Reuse and extend the existing suites for this component. New tests cover changed
behavior and real refusal boundaries; do not mirror every branch or create a new
test framework. Record actual commands, versions, inputs, exit codes and outputs.
The work order names the focused suite and evidence destination. Run the broad
suite on the integrated candidate; repeat only after relevant changes or failures.

## Evidence and completion

Retain the matrix assessment, resource identities, command output and meaningful
failures under the selected work order's evidence directory. Bind verification
to the exact clean committed candidate with the released capture procedure.
Preparation does not provide human acceptance. Integration CI and later public
release/adoption remain separate decisions.
