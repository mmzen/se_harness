+++
id = "VER-IAR-022"
type = "verification"
title = "Verify minimal installation and safe migration"
status = "approved"
owners = ["mmzen"]
created = "2026-09-30"
updated = "2026-09-30"

[relations]
verifies = ["REQ-IAR-031"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-30T11:12:12Z"
decided_by = "mmzen"
reason = "Human mmzen: I confirm and approve. Approves the updated external-resource package and required commit-bound verification for WO-IAR-028, WO-IAR-029 and WO-IAR-030. Clarification confirmed: Ok for this plan; short bootstrap before cloning, immediate activation of the actual checkout, per-session recovery after compaction/resume and independent parallel sessions. DEC-IAR-003 separately records future release and separate adoption. Reviewed file SHA-256 b9ef7eef837196d4100197ae384159946865ae206e5d59f691d1c72121a03717."
+++

# Verify minimal installation and safe migration

## Independence

Expected behavior comes from REQ-IAR-031, SPEC-IAR-016 and unchanged lifecycle/authority
contracts, not candidate output. Use an independently built candidate wheel outside
the checkout. Released 0.20.0 remains the governing evaluator for this work.

## Requirement-to-evidence matrix

| Requirement | Check | Pass condition |
| --- | --- | --- |
| REQ-IAR-031 | Fresh footprint | On an empty fixture, default initialization creates exactly the two selection files. Inspect the complete diff. Explicitly selected CI/PR/Git scaffolding creates only its reviewed files. Repeated setup is unchanged. |
| REQ-IAR-031 | Governed evidence | Create a small formal chain and run its authorized candidate-fixture lifecycle through verification preparation. Required Git byte rules are established explicitly before hash-bound writes; Windows/Linux evidence identities agree. |
| REQ-IAR-031 | Safe retirement | Upgrade an unmodified legacy fixture only after replacement delivery succeeds. Remove reviewed managed copies and explicitly selected stock seeds. Customized authoring/templates, symlinks and identity conflicts refuse before partial writes and preserve every owner byte. |
| REQ-IAR-031 | Recovery | Interrupt the existing migration transaction at its meaningful write boundary; inspect retained state and retry. Demonstrate rollback or resumable completion without losing the entry route or rewriting formal history. |
| REQ-IAR-031 | References and integrated behavior | Resolve all current resource links and classify historical references by release/commit. Check that the installation guide explains bootstrap, activation after cloning, recovery and parallel sessions using the implemented interface. Run the existing full suite once on the integrated candidate plus distribution validation, packaged CLI smoke and the native host scenarios in VER-IAR-021. Retain earlier failures, if any. |

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
