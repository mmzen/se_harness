+++
id = "VER-IAR-013"
type = "verification"
title = "Owner-region routing and context-action withdrawal evidence contract"
status = "approved"
owners = ["quality-owner", "security-owner"]
created = "2026-08-21"
updated = "2026-08-21"

[relations]
verifies = ["REQ-IAR-021"]
+++

# Verification Contract: Owner-region routing and context-action withdrawal evidence contract

## Independence

Expectations are derived from observable artifacts rather than from the implementation's own text:

- Rule-vocabulary stability is asserted by extracting the ordered `HRN-*` identifiers from the candidate router and comparing the sequence against the recorded baseline, not by asserting the revised prose.
- Routing completeness is asserted by checking that every subject row still has exactly one non-empty owner, not by asserting a specific owner string.
- Withdrawal of the reference-action form is asserted by feeding a fixture contract that declares it and requiring rejection, not by grepping for removed identifiers.
- Fragment integrity is asserted by recomputing `canonical_sha256(tracked_content("fragment", ...))` and comparing against `.engineering-harness.lock`, so the test fails on any drift including drift the implementer introduces deliberately.
- Managed-path expectations are derived from the lock, filtered by ownership mode, rather than enumerated in prose.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
|---|---|---|---|
| REQ-IAR-021.1 | automated test | candidate `ENGINEERING_HARNESS.md.tpl` content scan | the router names the owner-controlled region of `AGENTS.md` as the location of repository facts and commands, and names no scaffolded context document anywhere in the file |
| REQ-IAR-021.2 | automated test | candidate router stop-condition list | no stop condition references repository-context presence, completeness, or currency |
| REQ-IAR-021.3 | automated test | candidate router stop-condition list against baseline | every other baseline stop condition is present, including missing or damaged managed gate and owner-instruction conflict |
| REQ-IAR-021.4 | automated test | packaged `AGENTS.md.fragment` | the tracked block is byte-identical to the recorded baseline and names exactly one harness destination |
| REQ-IAR-021.5 | inspection | installation guidance | the owner responsibility for operational facts is stated exactly once across the router and the `init` sequence |
| REQ-IAR-021.6 | automated test | fixture contract declaring a reference step with an action identifier; fixture declaring a procedure identifier | the first is rejected before resolution with a diagnostic naming the withdrawn form; the second resolves with unchanged ordering and output |
| REQ-IAR-021.7 | automated test and inspection | governed-artifact scan | no active artifact describes the withdrawn document as a live obligation; every historical evidence, verification, and release record is unmodified |
| REQ-IAR-021.8 | automated test | owner-region content probe | no code path reads, parses, validates, or digests owner-region content outside the tracked fragment block |

## Acceptance scenarios

Added to the instruction-architecture acceptance feature:

1. An agent that has loaded only `CLAUDE.md` and `AGENTS.md` and consults the managed router is directed to the owner-controlled region for the repository test command, and to no scaffolded document.
2. A repository with no operational facts in its owner region is not stopped by any managed stop condition on repository context.
3. A candidate router that still names the withdrawn document fails the routing-content check and the failure identifies the line.
4. A workflow contract declaring a reference step with an action identifier fails conformance with a diagnostic naming the withdrawn form.
5. A contract declaring only procedure references produces byte-identical resolved procedures to the recorded baseline.

## Property and invariant tests

- **Rule-identity stability.** The ordered `HRN-*` sequence extracted from the candidate router equals the recorded baseline sequence. Identity and order are invariant; prose is not.
- **Routing totality.** Every routing-table subject has exactly one non-empty normative owner, and the subject set equals the baseline subject set.
- **Fragment digest invariance.** The computed fragment digest for every fragment-mode path equals its lock entry, before and after the change.
- **Resolver determinism.** For the full procedure corpus, resolved procedures are byte-identical to the baseline, establishing that removing the action branch changed no reachable behavior.
- **Unreachability confirmation.** No call site supplies a repository-context argument to the resolver, asserted by static inspection of the call graph before removal, so that the removal is documented as dead-path elimination rather than behavior change.
- **Owner-region non-interference.** For randomized owner-region content, including content resembling action markers and field labels, no diagnostic, digest, or validation outcome changes.

## Static and architecture checks

- `python scripts/validate_engineering_artifacts.py --root .` reports zero errors. Warnings are compared against the recorded baseline of 44 rather than an absolute expectation.
- After the supersessions and the operating-contract revision, the validator reports zero errors. A run showing `E017` on `OPS-IAR-001` is a failure of this contract, not an accepted condition.
- `REQ-IAR-003` remains active with its acceptance criterion revised and its status unchanged.
- The full unittest suite is compared against the recorded baseline, with the two known environment conditions named explicitly: the editable-install runtime-identity failure and the CRLF machine-contract comparison. Neither may be reported as a regression and neither may be used to excuse a new failure.
- The retained existing instruction-route tests continue to pass unmodified except where a baseline they assert has legitimately changed, and every such change is itemized in the evidence.

## Security and privacy checks

- Confirm no code path resolves an executable step from content outside harness governance, asserted by the absence of the action resolver and by the rejection fixture.
- Confirm the owner region is never parsed, validated, or hashed outside the tracked fragment block.
- Confirm the released-evaluator boundary is unchanged: the governing `doctor` verdict is produced by the released evaluator executed from outside the checkout, and the evaluator identity is recorded.

## Performance and resilience checks

- No performance expectation is asserted; the removed path is unreachable and the remaining changes are textual.
- Resilience: a malformed candidate router, a contract with a cyclic procedure reference, and a contract exceeding the reference depth each fail with their existing diagnostics and change no lifecycle state.

## Manual assessments

- The repository owner confirms that withdrawing the repository-context stop condition is intended, and that no replacement condition over ungoverned content is introduced.
- The technical owner records the architecture applicability decision for `ARCH-IAR-001` and whether a deciding ADR is required.
- The requirements steward confirms that superseding `REQ-IAR-005` and revising `REQ-IAR-003`, `REQ-WEX-010`, `SPEC-WEX-002`, and `VER-WEX-002` preserves the upstream trace to `INT-IAR-001` and `CAP-IAR-001`.
- The release owner confirms the migration note.
- All four are recorded before the work order leaves `draft`.

## Evidence retention

Retain under this domain's `evidence/` directory, keyed to the implementing work order:

- Candidate router before and after, with the extracted `HRN-*` sequence and routing-subject set for both.
- Computed and expected fragment digests for every fragment-mode path, before and after.
- The rejection diagnostic for the action-form fixture and the resolved-procedure corpus comparison.
- The static call-graph finding that no caller supplied the repository-context argument.
- Validator output before and after the supersessions and the operating-contract revision.
- Unittest output with the baseline comparison and both environment conditions named.
- Released-evaluator `doctor` output from outside the checkout, with the evaluator identity, alongside the in-tree run labelled as candidate-source drift evidence.
- Preflight output for both phases.
- The itemized list of governed artifacts revised, and the itemized list of historical records deliberately left unchanged.

## Residual uncertainty

- Whether any external consumer authored a `CTX-ACT-*` block is unknowable from this repository. The form is unreachable in the shipped resolver, so such a block never executed; the migration note is the only available mitigation.
- Whether an external consumer relied on the withdrawn stop condition cannot be measured. The compensating guidance directs them to state it in their own owner region.
- The candidate-versus-root drift on `ENGINEERING_HARNESS.md` persists until publication, so no in-tree `doctor` run can serve as a governing verdict for this change.
